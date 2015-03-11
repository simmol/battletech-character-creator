import kivy
kivy.require( '1.8.0' )

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string( """
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press:
                root.manager.current = 'settings'
                root.manager.transition.direction = 'left'
        Button:
            text: 'Quit'

<CharacterCreatorScreen>:
    BoxLayout:
        Button:
            text: 'Back to menu'
            on_press:
                root.manager.transition.direction = 'right'
                root.manager.current = 'menu'
        Button:
            text: 'My settings button'
""" )

class MenuScreen( Screen ):
    pass

class CharacterCreatorScreen( Screen ):
    pass

sm = ScreenManager()
sm.add_widget( MenuScreen( name='menu' ) )
sm.add_widget( CharacterCreatorScreen( name='settings' ) )


class CharacterCreatorApp( App ):

    def build( self ):
        return sm



