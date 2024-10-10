import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

import GraphScreen as GraphS
import DragAndDrop


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DragAndDrop.DragDropScreen(name='drag_drop'))
        sm.add_widget(GraphS.GraphScreen(name='graph'))
        sm.get_screen('graph').create_graphs()
        return sm

    def on_stop(self):
        if os.path.exists("graph.png"):
            os.remove("graph.png")