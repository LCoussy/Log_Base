# MainApp.py

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from pandas.core.window import Window  # Probablement une erreur d'import, devrait être `kivy.core.window.Window`
from DisplayArray import DisplayArray
from DragAndDrop import DragDropScreen  # Assuming this is another screen

class MainApp(App):
    """
    MainApp is the primary class for the Kivy application. It manages the app's screens using ScreenManager.
    It includes a drag-and-drop screen for file selection and a display array screen for data visualization.
    """

    def build(self):
        """
        Build the application by initializing the ScreenManager and adding screens for drag-and-drop functionality 
        and data display. This is the entry point for starting the app.

        Returns:
            ScreenManager: The manager handling navigation between app screens.
        """
        sm = ScreenManager()

        # Add the DragDropScreen to the ScreenManager
        sm.add_widget(DragDropScreen(name='drag_drop'))

        # Create and add the DisplayArray screen to the ScreenManager
        display_array_screen = DisplayArray(name='display_array')
        sm.add_widget(display_array_screen)

        return sm
