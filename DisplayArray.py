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
import GetContentLog

class DisplayArray(Screen):
    def __init__(self, type, **kwargs):
        super(DisplayArray, self).__init__(**kwargs)
        self.df_combined_lost = pd.DataFrame()  # Stocker les données pour réutilisation
        self.df_combined_blocked = pd.DataFrame()  # Stocker les données pour réutilisation
        self.myType = type
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        up_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)
        down_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=10, spacing=10)

        # Titre
        title = Label(
            text="Tableaux des logs : requetes " + self.myType,
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

    def update_table_blocked(self, selected_files):
        self.grid_layout.clear_widgets()
        self.df_combined_blocked = pd.DataFrame()

        for file in selected_files:

            # df = dh.create_table_blocked_request(parser.parse_log(file))
            fileParsedFiltered = dh.filter_request_datafile(GetContentLog.parse(file))
            df_blocked = dh.create_table_blocked_request(fileParsedFiltered.get('BLOCKED'))
            if df_blocked is not None and not df_blocked.empty:
                self.df_combined_blocked = pd.concat([self.df_combined_blocked, df_blocked], ignore_index=True)

        self.df_combined_blocked.drop_duplicates(inplace=True)
        self.df_combined_blocked.reset_index(drop=True, inplace=True)

        if not self.df_combined_blocked.empty:
            self.grid_layout.cols = self.df_combined_blocked.shape[1]
            for header in self.df_combined_blocked.columns:
                self.grid_layout.add_widget(Label(text=header, bold=True))
            for row in self.df_combined_blocked.values:
                for cell in row:
                    self.grid_layout.add_widget(Label(text=str(cell)))

    def update_table_lost(self, selected_files):
        self.grid_layout.clear_widgets()
        self.df_combined_lost = pd.DataFrame()

        for file in selected_files:

            # df = dh.create_table_blocked_request(parser.parse_log(file))
            fileParsedFiltered = dh.filter_request_datafile(GetContentLog.parse(file))
            df_lost = dh.create_table_lost_request(fileParsedFiltered.get('LOST'))
            if df_lost is not None and not df_lost.empty:
                self.df_combined_lost = pd.concat([self.df_combined_lost, df_lost], ignore_index=True)

        self.df_combined_lost.drop_duplicates(inplace=True)
        self.df_combined_lost.reset_index(drop=True, inplace=True)

        if not self.df_combined_lost.empty:
            self.grid_layout.cols = self.df_combined_lost.shape[1]
            for header in self.df_combined_lost.columns:
                self.grid_layout.add_widget(Label(text=header, bold=True))
            for row in self.df_combined_lost.values:
                for cell in row:
                    self.grid_layout.add_widget(Label(text=str(cell)))
