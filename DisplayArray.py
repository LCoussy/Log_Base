# DisplayArray.py
import os

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView

import pandas as pd
from kivy.clock import Clock

import parser as par
import data_handler as dh

from DisplayLogs import LogExplorer


class DisplayArray(Screen):
    def __init__(self, **kwargs):
        super(DisplayArray, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        grid_layout = GridLayout(size_hint=(1, 0.9), padding=10, spacing=10, row_force_default=True,
                                 row_default_height=40)

        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        # Left Layout: LogExplorer (TreeView)
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=10, spacing=10)

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        log_directory = ""
        self.log_explorer = LogExplorer(
            log_directory=log_directory,
            on_files_selected=self.updateTable
        )
        left_layout.add_widget(self.log_explorer)

        title = Label(
            text="Tableaux des logs",
            size_hint=(1, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        right_layout.add_widget(up_layout)

        right_layout.add_widget(grid_layout)

        # Assemble the main layout
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def updateTable(self, selected_files):
        self.grid_layout.clear_widgets()
        df_combined = pd.DataFrame()

        for file in selected_files:
            df = dh.createTableBlockedRequest(par.parse_log(file))

            if df is not None and not df.empty:
                df_combined = pd.concat([df_combined, df], ignore_index=True)

        for file in selected_files:
            df = dh.createTableBlockedRequest(par.parse_log(file))

        # enlève les duplica après la fusion
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
