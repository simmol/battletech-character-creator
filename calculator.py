"""
A base version of calculating Character Attributes, Traits and Skills based on Live module choices made
TODO Should look later into this how can be re-factored and made more stable
For now this is as straight forward as possible
"""

import yaml
from collections import OrderedDict

# Get base stats and values
with open( 'data/base_stats.yaml', 'r' ) as f:
    attributes = yaml.load( f )


# Get Affiliations data
with open( 'data/affiliations.yaml', 'r' ) as f:
    affiliations = yaml.load( f )

#
# Affiliation
#

#TODO implement affiliation choice
affiliation_choice = "Terran"
affiliation = affiliations[affiliation_choice]

#TODO implement Sub-affiliation choice
sub_affiliation_choice = 'Belter'
sub_affiliation = affiliation['Sub-Affiliations'][sub_affiliation_choice]

fixed_xp = affiliation['Fixed XP']

# Player Attributes
player_attr = attributes
for attr, value in attributes.iteritems():
    #TODO handle EXTRA Attribute choices
    try:
        # Base Affiliation
        player_attr[attr] = player_attr[attr] + fixed_xp['Attributes'][attr]
    except KeyError:
        pass

    try:
        # Sub-Affiliation
        player_attr[attr] = player_attr[attr] + sub_affiliation['Attributes'][attr]
    except KeyError:
        pass

print player_attr

# Player Traits
player_traits = OrderedDict()

for trait, value in affiliation['Fixed XP']['Traits'].iteritems():
    if trait is not 'CHOICE':
        player_traits[trait] = player_traits.get(trait, 0) + value


for trait, value in sub_affiliation['Traits'].iteritems():
    if trait != 'CHOICE':
        player_traits[trait] = player_traits.get(trait, 0) + value

print player_traits
