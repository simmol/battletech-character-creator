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

def collect_skill_names( base, module ):
    for skill, value in  module['Fixed XP']['Skills'].iteritems():
        if 'CHOICE' in skill:
            for key in value['list']:
                military_skills.append( key )
        else:
            military_skills.append( skill )


class Player():

    def __init__( self, name, start_xp = 4150 ):
        self.name = name
        self.age  = 16
        self.xp_pool = start_xp

        self.flexible_xp = {
            'value': 0, # XXX May rename in the future but i don't want to change all data files now
            'attributes': 0,
            'traits': 0,
            'skills': 0,
            'special': []
        }

        self.attributes = get_base_attributes()
        self.traits     = {}
        self.skills     = { 'Language/English':20, 'Perception':10, 'Language/Affiliation': 20 }

        self.choices = {
            'Attributes': [],
            'Traits': [],
            'Skills': [],
        }


    def __getitem__( self, name ):
        return getattr( self, name )

    def __setitem__( self, name, value ):
        setattr( self, name, value )

    def get( self, name, default = None ):
        try:
            return getattr( self, name )
        except AttributeError:
            return default


    def normalize_character_stats( self ):
        """ At the end of character creation no Attribute should be below 1 
            The idea is to up the character Stats to at least 1 using Flexible XP and left XP Pool
            This is mendatory step so we can make it automatic
        """
        #TODO Implement this
        pass


class Calculator():

    def __init__( self, the_player ):
        self.base   = the_player
        self.player = deepcopy( the_player ) # We make a copy of the player, so we don't make accidental override

        self.life_modules = []

    def calculate_module( self, module ):
        """ Calculate accumulation of stats for the module: Attributes, Traits and Skills """

        for key in ["Attributes", "Traits", "Skills"]:
            stats = module.get( key, None )
            if not stats:
                continue

            for stat, value in stats.iteritems():
                if not isinstance( value, dict ):
                    self.player[key.lower()][stat] = self.player[key.lower()].get( stat, 0 ) + value

                if 'CHOICE' in stat:
                    self.player.choices[key].append( value )




    def apply_changes( self ):
        """ We apply the changes to the real Player object """
        self.base.attributes = self.player.attributes
        self.base.traits     = self.player.traits
        self.base.skills     = self.player.skills
        self.base.xp_pool    = self.player.xp_pool
        self.base.choices    = self.player.choices



def calc( base, module ):

    # Extract module cost
    base.xp_pool = base.xp_pool - module.get( 'cost', 0 )

    # Calculate base XP for Attr, Traits and Skills
    calculator = Calculator( base )
    calculator.calculate_module( module['Fixed XP'] )

    # Set the calculated changes in the Player object
    calculator.apply_changes()

    # TODO Revise this to implemente Stage restrictions to Flexible XP
    # During Stage 2, a character may spend no
    # more than 35 flexible XPs on a single Skill, and no more than
    # 200 flexible XPs on any one Attribute or Trait.

    module_flexible_xp = module.get( 'Flexible XP', {})
    if module_flexible_xp.get( 'limit' ):
        base.flexible_xp['special'].append( module_flexible_xp )
    else:
        for key, _ in base.flexible_xp.iteritems():
            if key != 'special':
                base.flexible_xp[key] = base.flexible_xp[key] + module_flexible_xp.get( key, 0 )



#
# Base
#

player = Player( "Simmol" )


# TODO Collect in player - Flexible XP categorized by from where it comes and how should be used
# So we can provide a step to distribute it after all basic XP is calculated
# TODO Handle Flexible XP requirements


# TODO Implement Life Module selection steps

#
# STAGE 0 - Affiliation
#

# Get Affiliations data
with open( 'data/affiliations.yaml', 'r' ) as f:
    affiliations = yaml.load( f )

affiliation_choice = "Terran"
affiliation = affiliations[affiliation_choice]

sub_affiliation_choice = 'Belter'
sub_affiliation = affiliation['Sub-Affiliations'][sub_affiliation_choice]

# Affiliation
calc( player, affiliation )

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

calc( player, early_childhood )

#
# STAGE 2 - Late Childhood
#

# Get Late Childhood data
with open( 'data/late_childhood.yaml', 'r' ) as f:
    late_childhoods = yaml.load( f )

late_childhood_choice = "SPACER FAMILY"
late_childhood = late_childhoods[late_childhood_choice]

calc( player, late_childhood )

#
# STAGE 3 - HIGHER EDUCATION
#
# TODO Each "TYPE" of module ( School ) in this stage can be taken 1 time to accumulate 3 modules
# Example: player can pick one "Military",  one "Civilian" and one "Intelligence/Police School"

with open( 'data/higher_education.yaml', 'r' ) as f:
    higher_educations = yaml.load( f )

higher_education_choice = "Military Enlistment"
higher_education = higher_educations[higher_education_choice]

# Only 3 fields per School
basic_field     = "Basic Training ( Naval )" # XXX Required
advanced_field  = "Technician/Military" # XXX Required
special_field   = "Technician/Vehicle" # XXX Optional Can be one from Advanced or Special fields

calc( player, higher_education )

# Calculate Choosen Fields Skill earned and age
with open( 'data/master_fields_list.yaml', 'r' ) as f:
    master_fields_list = yaml.load( f )

calc( player, master_fields_list[basic_field] )
calc( player, master_fields_list[advanced_field] )

player.age = player.age + higher_education['Fields']['Basic']['age']
player.age = player.age + higher_education['Fields']['Advanced']['age']

if special_field: # This one may be missing
    calc( player, master_fields_list[special_field] )
    player.age = player.age + higher_education['Fields']['Special']['age']


# Collect Military and Civilian Skills based on Choosen Fields
military_skills = []
if higher_education['type'] == "Military":
    collect_skill_names( military_skills, master_fields_list[basic_field] )
    collect_skill_names( military_skills, master_fields_list[advanced_field] )
    collect_skill_names( military_skills, master_fields_list[special_field] )


#
# STAGE 4 - Real Life
#

with open( 'data/real_life.yaml', 'r' ) as f:
    real_life_modules = yaml.load( f )

real_life_choice = "TOUR OF DUTY"
real_life = real_life_modules[real_life_choice]

calc( player, real_life )
player.age = player.age + real_life['age']

# XXX For now handle it as special case
if real_life_choice == "TOUR OF DUTY": # See what part of the data to use based on choosen "Affiliation type"
    calc( player, real_life[affiliation['category']] )


###
### Print
###
print "Name: ", player.get( "name" )
print "Age: ", player.get( "age" )
print "XP Pool: ", player.get( "xp_pool" )
print "Attributes", player.get( "attributes" )
print "Traits", player.get( "traits" )
print "Skills", player.get( "skills" )

print "Flexible XP", player.flexible_xp
print "Choices: ", player.choices
