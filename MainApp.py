#MainApp.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button

from DragAndDrop import DragDropScreen
from Display import Display
from HandleSwitch import HandleSwitch

from kivy.uix.button import Button

class MainApp(App):
    def build(self):
        sm = ScreenManager()

        # Drag and Drop screen
        dragDropScreen = DragDropScreen(name='drag_drop')
        sm.add_widget(dragDropScreen)

        # Display Block screen
        display_block_screen = Display(name='displayBlock', type='B', fileOrDirectoryPath=dragDropScreen.path)
        sm.add_widget(display_block_screen)

        # Display Lost screen
        display_lost_screen = Display(name='displayLost', type='L', fileOrDirectoryPath=dragDropScreen.path)
        sm.add_widget(display_lost_screen)

        # Add separate HandleSwitch instances to each screen
        handle_switch_block = HandleSwitch(sm,'displayLost')
        display_block_screen.add_widget(handle_switch_block)

        handle_switch_lost = HandleSwitch(sm,'displayBlock')
        display_lost_screen.add_widget(handle_switch_lost)

        return sm


    def go_to_lost_page(self, instance):
        """
        Navigue vers la page displayLost lorsqu'on appuie sur le bouton global.
        """
        self.root.current = 'displayLost'

    def go_to_block_page(self, instance):
        """
        Navigue vers la page displayBlock lorsqu'on appuie sur le bouton global.
        """
        self.root.current = 'displayBlock'