#MainApp.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button

from DragAndDrop import DragDropScreen
from Display import Display
from DisplayStat import DisplayStat

from kivy.uix.button import Button

class MainApp(App):
    def build(self):
        # Display Block screen
        sm = ScreenManager()
        dragDropScreen = DragDropScreen(name='drag_drop')
        sm.add_widget(dragDropScreen)

        # Create and add DisplayArray Screen
        display_screen = Display(name='display', fileOrDirectoryPath=dragDropScreen.path)
        sm.add_widget(display_screen)



        return sm
