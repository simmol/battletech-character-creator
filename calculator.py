"""
A base version of calculating Character Attributes, Traits and Skills based on Live module choices made
TODO Should look later into this how can be re-factored and made more stable
For now this is as straight forward as possible
"""

# TODO Collect in player - Flexible XP categorized by from where it comes and how should be used
# So we can provide a step to distribute it after all basic XP is calculated
# TODO Handle Flexible XP requirements
# TODO Implement Life Module selection steps



import yaml
from copy import deepcopy

from load_data import get_affiliations, get_early_childhoods, get_late_childhoods, get_higher_education, get_master_fields_list, get_real_life_modules, get_base_attributes



def collect_skill_names( base, module ):
    for skill, value in  module['Fixed XP']['Skills'].iteritems():
        if 'CHOICE' in skill:
            for key in value['list']:
                base.append( key )
        else:
            base.append( skill )


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


class LifeModules():

    def __init__( self ):
        self.affiliation        = None
        self.sub_affiliation    = None
        self.early_childhood    = None
        self.late_childhood     = None
        self.higher_education   = None
        self.real_life          = []

        self.military_skills    = []


    def calculate_affiliation( self, affiliation_choice ):
        # Affiliation
        affiliations = get_affiliations()
        self.affiliation = affiliations[affiliation_choice]

        calc( player, self.affiliation )


    def calculate_sub_affiliation( self, affiliation_choice, sub_affiliation_choice ):
        # Sub-Affiliation
        affiliations = get_affiliations()
        affiliation = affiliations[affiliation_choice]

        self.sub_affiliation = affiliation['Sub-Affiliations'][sub_affiliation_choice]
        calc( player, self.sub_affiliation )


    def calculate_early_childhood( self, early_childhood_choice ):

        early_childhoods = get_early_childhoods()
        self.early_childhood = early_childhoods[early_childhood_choice]

        calc( player, self.early_childhood )


    def calculate_late_childhood( self, late_childhood_choice ):
        late_childhoods = get_late_childhoods()
        self.late_childhood = late_childhoods[late_childhood_choice]

        calc( player, self.late_childhood )


    def calculate_higher_education( self, higher_education_choice, field_choices ):
        higher_educations = get_higher_education()
        self.higher_education = higher_educations[higher_education_choice]

        calc( player, self.higher_education )


        # Calculate Choosen Fields Skill earned and age
        # Only 3 fields per School
        basic_field     = field_choices['basic']                # "Basic Training ( Naval )" # XXX Required
        advanced_field  = field_choices['advanced']             # "Technician/Military" # XXX Required
        special_field   = field_choices.get('special', None)    # "Technician/Vehicle" # XXX Optional Can be one from Advanced or Special fields

        master_fields_list = get_master_fields_list()

        calc( player, master_fields_list[basic_field] )
        calc( player, master_fields_list[advanced_field] )

        player.age = player.age + self.higher_education['Fields']['Basic']['age']
        player.age = player.age + self.higher_education['Fields']['Advanced']['age']

        if special_field: # This one may be missing
            calc( player, master_fields_list[special_field] )
            player.age = player.age + self.higher_education['Fields']['Special']['age']


        # Collect Military and Civilian Skills based on Choosen Fields
        if self.higher_education['type'] == "Military":
            collect_skill_names( self.military_skills, master_fields_list[basic_field] )
            collect_skill_names( self.military_skills, master_fields_list[advanced_field] )
            collect_skill_names( self.military_skills, master_fields_list[special_field] )


    def calculate_real_life_module( self, real_life_choice ):
        real_life_modules = get_real_life_modules()

        real_life = real_life_modules[real_life_choice]
        self.real_life.append( real_life )

        calc( player, real_life )
        player.age = player.age + real_life['age']

        # XXX For now handle it as special case
        if real_life_choice == "TOUR OF DUTY": # See what part of the data to use based on choosen "Affiliation type"
            calc( player, real_life[self.affiliation['category']] )

#
# Base
#

player = Player( "Simmol" )
life_modules = LifeModules()

#
# STAGE 0 - Affiliation
#

life_modules.calculate_affiliation('TERRAN')

#
# STAGE 1 - Early Childhood
#

life_modules.calculate_early_childhood('BLUE COLLAR')

#
# STAGE 2 - Late Childhood
#

life_modules.calculate_late_childhood('SPACER FAMILY')

#
# STAGE 3 - HIGHER EDUCATION
#
# TODO Each "TYPE" of module ( School ) in this stage can be taken 1 time to accumulate 3 modules
# Example: player can pick one "Military",  one "Civilian" and one "Intelligence/Police School"

master_field_choices = {
    'basic'     : "Basic Training ( Naval )",
    'advanced'  : "Technician/Military",
    'special'   : "Technician/Vehicle",
}
life_modules.calculate_higher_education('MILITARY ENLISTMENT', master_field_choices)

#
# STAGE 4 - Real Life
#
# TODO Each Real Life module can be taken multiple times, but no Fixed XP is applied if the module is taken before

life_modules.calculate_real_life_module('TOUR OF DUTY')



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
