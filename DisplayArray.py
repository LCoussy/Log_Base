# DisplayArray.py
import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget


import pandas as pd

import parser
import data_handler as dh

class DisplayArray(Screen):
    def __init__(self, type, **kwargs):
        super(DisplayArray, self).__init__(**kwargs)
        self.df_combined = pd.DataFrame()  # Stocker les données pour réutilisation
        self.myType = type
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        up_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)
        down_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=10, spacing=10)

        # Titre
        title = Label(
            text="Tableaux des logs",
            size_hint=(0.8, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        # Tableau scrollable
        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.grid_layout = GridLayout(size_hint_y=None, padding=10, spacing=10, row_force_default=True, row_default_height=40)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        scroll_view.add_widget(self.grid_layout)

        down_layout.add_widget(scroll_view)

        main_layout.add_widget(up_layout)
        main_layout.add_widget(down_layout)
        self.add_widget(main_layout)

    def update_table(self, selected_files):
        self.grid_layout.clear_widgets()
        self.df_combined = pd.DataFrame()

        for file in selected_files:
            df = dh.create_table_blocked_request(parser.parse_log(file))
            if df is not None and not df.empty:
                self.df_combined = pd.concat([self.df_combined, df], ignore_index=True)

        self.df_combined.drop_duplicates(inplace=True)
        self.df_combined.reset_index(drop=True, inplace=True)

        if not self.df_combined.empty:
            self.grid_layout.cols = self.df_combined.shape[1]
            for header in self.df_combined.columns:
                self.grid_layout.add_widget(Label(text=header, bold=True))
            for row in self.df_combined.values:
                for cell in row:
                    self.grid_layout.add_widget(Label(text=str(cell)))
