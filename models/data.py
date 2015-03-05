import json
from collections import OrderedDict

from models.db import session
from models.base import Affiliation, SubAffiliation, Languages


new_language = Languages( name = 'English' )
session.add( new_language )
session.commit()

new_second_language = Languages( name = 'German' )
session.add( new_second_language )
session.commit()

affiliation_fixed_xp = OrderedDict()
affiliation_fixed_xp['Attributes'] = { 'INT': '+100', 'EDG': '-150', 'EXTRA': { 'value' : '+50', 'how_many': 2, 'exception': [ 'INT', 'EDG' ] } }
affiliation_fixed_xp['Traits']    = { 'Compulsion/Distrust of Non-Terrans': '-75', 'Reputation': '+100' }
affiliation_fixed_xp['Skills']    = { 'Language/English': '+25', 'Language/Any': '+15' }


fixed_xp = OrderedDict()

fixed_xp['Attributes']  = { 'STR': '-25', 'BOD': '-25', 'EXTRA': {'value': '+100', 'how_many': 1, 'exception': ['CHA', 'EDG'] } }
fixed_xp['Traits']      = { 'Compulsion/Xenophobia': '-100', 'Reputation': '-50', 'Wealth': '+50', 'CHOICE': {
    'traits': [ 'Ambidextrous', 'Attractive', 'Exeption Attribute/Any', 'Fast Learner', 'G-Tolerance', 'Good Hearing', 'Good Vision', 'Implant/Prosthetics', 'Pain Resistance', 'Toughness' ],
    'value': '+50' } }


fixed_xp_json = json.dumps( fixed_xp )
new_sub_affiliation = SubAffiliation( name = "Belter", fixed_xp = fixed_xp_json )
session.add( new_sub_affiliation )
session.commit()

affiliation_fixed_xp_json = json.dumps( affiliation_fixed_xp )
new_affiliation = Affiliation( name = "Terran", fixed_xp = affiliation_fixed_xp_json, primary_language=new_language.id, secondary_language=new_second_language.id, sub_affiliation=new_sub_affiliation.id, module_cost = 240 )

session.add( new_affiliation )
session.commit()
