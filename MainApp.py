import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager

import GraphScreen as GraphS
from DragAndDrop import DragDropScreen
from DisplayLogs import LogExplorer

class MainApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='horizontal')
        log_directory = "/home/egiraud/Téléchargements/log"

        log_explorer = LogExplorer(log_directory=log_directory)
        main_layout.add_widget(log_explorer)

        sm = ScreenManager()
        sm.add_widget(DragDropScreen(name='drag_drop'))
        sm.add_widget(GraphS.GraphScreen(name='graph'))
        sm.get_screen('graph').create_graphs()

        main_layout.add_widget(sm)

        return main_layout

    def on_stop(self):
        if os.path.exists("graph.png"):
            os.remove("graph.png")


