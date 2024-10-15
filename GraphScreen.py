from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
import parser as par
import data_handler as dh

import pandas as pd
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

import matplotlib.pyplot as plt

class GraphScreen(Screen):
    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=10, spacing=10)

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        grid_layout = GridLayout(size_hint=(1, 0.9), padding=10, spacing=10,row_force_default=True, row_default_height=40)

        title = Label(
            text="Tableaux des logs",
            size_hint=(1, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        df = (dh.createTableBlockedRequest(par.parse_log("GCE_10-30-02_17_07-10-2024.txt")))

        grid_layout.cols=df.shape[1]

        for headers in df.columns:
            grid_layout.add_widget(Label(text=headers, bold=True))

        for row in df.values:
            for cell in row:
                grid_layout.add_widget(Label(text=cell))

        right_layout.add_widget(up_layout)

        right_layout.add_widget(grid_layout)

        btn_to_main = Button(
            text="Retour au Menu",
            size_hint=(0.6, None),
            height=50,
            pos_hint={'center_x': 0.5},
            font_size='16sp'
        )
        btn_to_main.bind(on_release=self.go_to_main)
        left_layout.add_widget(btn_to_main)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def create_graphs(self):
        plt.figure(figsize=(5, 5))
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30], label=f'Graph')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Mon Graphique')
        plt.legend()
        filename = f"graph.png"
        plt.savefig(filename)
        plt.close()

    def go_to_main(self, instance):
        self.manager.current = 'drag_drop'

