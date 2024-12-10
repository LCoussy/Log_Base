# MainApp.py

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
# from pandas.core.window import Window

from DragAndDrop import DragDropScreen  # Assuming this is another screen
from Display import Display


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
        dragDropScreen = DragDropScreen(name='drag_drop')
        sm.add_widget(dragDropScreen)

        # Create and add DisplayArray Screen
        display_screen = Display(name='display', fileOrDirectoryPath=dragDropScreen.path)
        sm.add_widget(display_screen)

        return sm


