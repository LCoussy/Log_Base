#MainApp.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button

from DragAndDrop import DragDropScreen
from Display import Display

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

        # Créer un bouton pour chaque écran
        display_block_screen.add_widget(Button(
            text="Voir les Lost",
            size_hint=(1, 0.1),
            on_press=self.go_to_lost_page
        ))

        display_lost_screen.add_widget(Button(
            text="Voir les Block",
            size_hint=(1, 0.1),
            on_press=self.go_to_block_page
        ))

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