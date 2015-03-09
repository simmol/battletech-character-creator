"""
A base version of calculating Character Attributes, Traits and Skills based on Live module choices made
TODO Should look later into this how can be re-factored and made more stable
For now this is as straight forward as possible
"""

import yaml
from copy import copy, deepcopy
from collections import OrderedDict


def get_base_attributes():
    # Get base stats and values
    with open( 'data/base_stats.yaml', 'r' ) as ff:
        attributes = yaml.load( ff )

    return attributes


class Player():

    def __init__( self, name ):
        self.name = name
        self.age  = 16
        self.attributes = get_base_attributes()
        self.traits     = {}
        self.skills     = {}

    def __getitem__( self, name ):
        return getattr( self, name )

    def __setitem__( self, name, value ):
        setattr( self, name, value )

    def get( self, name, default = None ):
        try:
            return getattr(self, name)
        except AttributeError:
            return default



class Calculator():

    def __init__( self, player ):
        self.base   = player
        self.player = deepcopy( player ) # We make a copy of the player, so we don't make accidental override

        self.life_modules = []

    def calculate_module( self, module ):

        for key in ["Attributes", "Traits", "Skills"]:
            stats = module.get(key, None)
            if not stats:
                return

            for stat, value in stats.iteritems():
                if not isinstance( value, dict ):
                    self.player[key.lower()][stat] = self.player[key.lower()].get( stat, 0 ) + value


    def apply_changes( self ):
        """ We override """
        self.base.attributes = self.player.attributes
        self.base.traits     = self.player.traits
        self.base.skills     = self.player.skills



def calc( base, module ):

    calculator = Calculator( base )
    calculator.calculate_module( module )

    # Set the calculated changes in the Player object
    calculator.apply_changes()


#
# Base
#


player = Player( "Simmol" )

# TODO Collect in player - Flexible XP categorized by from where it comes and how should be used
# So we can provide a step to distribute it after all basic XP is calculated
# TODO Handle Flexible XP requirements

#
# STAGE 0 - Affiliation
#

# Get Affiliations data
with open( 'data/affiliations.yaml', 'r' ) as f:
    affiliations = yaml.load( f )

#TODO implement affiliation choice
affiliation_choice = "Terran"
affiliation = affiliations[affiliation_choice]

#TODO implement Sub-affiliation choice
sub_affiliation_choice = 'Belter'
sub_affiliation = affiliation['Sub-Affiliations'][sub_affiliation_choice]


# Affiliation
calc( player, affiliation['Fixed XP'] )

# Sub-Affiliation
calc( player, sub_affiliation )

#
# STAGE 1 - Early Childhood
#

# Get Early Childhood
with open( 'data/early_childhood.yaml', 'r' ) as f:
    early_childhoods = yaml.load( f )

early_childhood_choice = "BLUE COLLAR"
early_childhood = early_childhoods[early_childhood_choice]

calc( player, early_childhood['Fixed XP'] )

#
# STAGE 2 - Late Childhood
#

# Get Late Childhood data
with open( 'data/late_childhood.yaml', 'r' ) as f:
    late_childhoods = yaml.load( f )

late_childhood_choice = "SPACER FAMILY"
late_childhood = late_childhoods[late_childhood_choice]

calc( player, late_childhood['Fixed XP'] )

#
# STAGE 3 - HIGHER EDUCATION
#

with open( 'data/higher_education.yaml', 'r' ) as f:
    higher_educations = yaml.load( f )

# TODO implement Choices
# TODO This module can be taken more then 1
higher_education_choice = "Military Enlistment"
higher_education = higher_educations[higher_education_choice]

# Only 3 fields per School
basic_field     = "Basic Training ( Naval )" # XXX Required
advanced_field  = "Technician/Military" # XXX Required
special_field   = "Technician/Vehicle" # XXX Optional Can be one from Advanced or Special fields

calc( player, higher_education['Automatic'] )
# TODO Implement Fields and There skills

# TODO Calc Age based on how much and what fields are selected


#
# STAGE 4 - Real Life
#

with open( 'data/real_life.yaml', 'r' ) as f:
    real_life_modules = yaml.load( f )

real_life_choice = "TOUR OF DUTY"
real_life = real_life_modules[real_life_choice]

calc( player, real_life['Fixed XP'] )

# XXX For now handle it as special case
if real_life_choice == "TOUR OF DUTY": # See what part of the data to use based on choosen "Affiliation type"
    calc( player, real_life[ affiliation['category'] ] )


###
### Print
###
print "Name: ", player.get("name")
print "Age: ", player.get("age")
print "Attributes", player.get("attributes")
print "Traits", player.get("traits")
print "Skills", player.get("skills")

