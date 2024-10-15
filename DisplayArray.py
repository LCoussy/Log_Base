from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from pandas.core.interchange.dataframe_protocol import DataFrame

import parser as par
import data_handler as dh

import pandas as pd
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

import matplotlib.pyplot as plt

class DisplayArray(Screen):
    grid_layout = GridLayout(size_hint=(1, 0.9), padding=10, spacing=10, row_force_default=True, row_default_height=40)
    def __init__(self,**kwargs):
        super(DisplayArray, self).__init__(**kwargs)
        self.build_ui()


    def build_ui(self):
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=10, spacing=10)

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)


        title = Label(
            text="Tableaux des logs",
            size_hint=(1, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        # df = (dh.createTableBlockedRequest(par.parse_log("GCE_10-30-02_17_07-10-2024.txt")))


        right_layout.add_widget(up_layout)

        right_layout.add_widget(self.grid_layout)

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

    def go_to_main(self, instance):
        self.manager.current = 'log_screen'

    def updateTable(self, selected_files):
        self.grid_layout.clear_widgets()
        df_combined = pd.DataFrame()

        for file in selected_files:
            df = dh.createTableBlockedRequest(par.parse_log(file))

            if df is not None and not df.empty:
                df_combined = pd.concat([df_combined, df], ignore_index=True)

        for file in selected_files:
            df = dh.createTableBlockedRequest(par.parse_log(file))

        #enlève les duplica après la fusion
        df_combined.drop_duplicates(inplace=True)
        df_combined.reset_index(drop=True, inplace=True)
        df_combined.dropna(inplace=True)

        if not df_combined.empty:
            self.grid_layout.cols = df_combined.shape[1]
            for headers in df_combined.columns:
                self.grid_layout.add_widget(Label(text=headers, bold=True))
            for row in df_combined.values:
                for cell in row:
                    self.grid_layout.add_widget(Label(text=str(cell)))