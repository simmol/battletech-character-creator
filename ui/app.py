import kivy
kivy.require( '1.8.0' )

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button

Builder.load_string( """
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto Character Creation'
            on_press:
                root.manager.current = 'settings'
                root.manager.transition.direction = 'left'
        Button:
            text: 'Quit'
""" )

class MenuScreen( Screen ):
    pass


class CharacterCreatorScreen( Screen ):
    pass

from calculator import get_affiliations

def select_affiliation( instance ):
    print "Affiliation %s is selected" % instance.text

sm = ScreenManager()
sm.add_widget( MenuScreen( name='menu' ) )
character_create = CharacterCreatorScreen( name='settings' )
sm.add_widget( character_create )

box_layout  = GridLayout()
box_layout.cols = 4
box_layout.rows = 4

dropdown = DropDown()
dropdown_list = get_affiliations()

for key in dropdown_list.keys():
    btn = Button( text = ' %s ' % key, size_hint_y=None, height=44 )
    btn.bind( on_release=lambda btn: dropdown.select( btn.text ) )
    btn.bind( on_press=select_affiliation )
    dropdown.add_widget( btn )

dropdown_button = Button( text='Pick Affiliation', size_hint= ( None,None ), height = 44 )
dropdown_button.bind( on_release=dropdown.open )
dropdown.bind( on_select=lambda instance, x: setattr( dropdown_button, 'text', x ) )


box_layout.add_widget( dropdown_button )

character_create.add_widget( box_layout )


class CharacterCreatorApp( App ):

    def build( self ):
        return sm



