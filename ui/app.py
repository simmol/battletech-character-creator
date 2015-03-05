import kivy
kivy.require( '1.8.0' )

from kivy.app import App
from kivy.uix.gridlayout import GridLayout

class CharacterCreator( GridLayout ):

    def __init__(self, **kwargs):
        super(CharacterCreator, self).__init__(**kwargs)
        self.cols = 2

class CharacterCreatorApp( App ):

    def build(self):
        return CharacterCreator()

