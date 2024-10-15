import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

from DisplayArray import DisplayArray
from DragAndDrop import DragDropScreen
from DisplayLogs import LogExplorer
from kivy.uix.screenmanager import Screen


class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='horizontal')
        log_directory = ""

        log_explorer = LogExplorer(log_directory=log_directory)

        sm = ScreenManager()
        sm.add_widget(DragDropScreen(name='drag_drop'))

        # Ajoutez l'écran de logs ici
        log_screen = Screen(name='log_screen')
        log_screen.add_widget(log_explorer)  # Ajouter l'explorateur de logs dans cet écran
        sm.add_widget(log_screen)

        # sm.get_screen('array').create_graphs()

        sm.add_widget(DisplayArray(name='array'))
        # sm.get_screen('array').create_arrayS()

        main_layout.add_widget(sm)

        return main_layout

    def on_stop(self):
        if os.path.exists("graph.png"):
            os.remove("graph.png")