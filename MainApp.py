# MainApp.py

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from pandas.core.window import Window

from DisplayArray import DisplayArray
from DragAndDrop import DragDropScreen  # Assuming this is another screen


class MainApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(DragDropScreen(name='drag_drop'))

        # Create and add DisplayArray Screen
        display_array_screen = DisplayArray(name='display_array')
        sm.add_widget(display_array_screen)

        return sm


