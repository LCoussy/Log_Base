# Display.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from DisplayData import DisplayData
from DisplayArray import DisplayArray
from batchOpen import batchOpen
from DisplayLogTree import LogExplorer
from kivy.app import App
import pandas as pd

import data_handler as dh
import GetContentLog

class Display(Screen):
    """
    Screen that contains the DisplayArray and manages its layout.
    """

    def __init__(self, fileOrDirectoryPath, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.df_combined_lost_data = pd.DataFrame()  # Stock datas
        self.df_combined_blocked_data = pd.DataFrame()  # Stock datas
        self.fileOrDirectoryPath = fileOrDirectoryPath
        self.build_ui()

    def build_ui(self):
        """
        Build the user interface of the Display screen.
        """
        main_layout = BoxLayout(orientation='horizontal', padding=0, spacing=0)
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)
        switchGraphButton = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=10, spacing=10)
        logTreeLayout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=10, spacing=10)

        left_layout.add_widget(logTreeLayout)
        left_layout.add_widget(switchGraphButton)
        self.displayData = DisplayData()
        self.logExplorer = LogExplorer(log_directory=self.fileOrDirectoryPath, on_file_selected=self.on_file_selected)

        logTreeLayout.add_widget(self.logExplorer)
        right_layout.add_widget(self.displayData)
        switchGraphButton.add_widget(self.displayData.handleSwitchGraph)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        self.add_widget(main_layout)


    def on_file_selected(self, selected_files):
        """
        Callback function to handle file selection in LogExplorer.

        Args:
            selected_files (list of str): List of selected file paths.
        """
        for file in selected_files:

            df_blocked = dh.create_table_blocked_request(GetContentLog.parse(file).get('BLOCKED'))
            if df_blocked is not None and not df_blocked.empty:
                self.df_combined_blocked_data = pd.concat([self.df_combined_blocked_data, df_blocked], ignore_index=True)
            df_lost = dh.create_table_lost_request(GetContentLog.parse(file).get('LOST'))
            if df_lost is not None and not df_lost.empty:
                self.df_combined_lost_data = pd.concat([self.df_combined_lost_data, df_lost], ignore_index=True)

        self.df_combined_lost_data.drop_duplicates(inplace=True)
        self.df_combined_lost_data.reset_index(drop=True, inplace=True)

        print("-------------------\n", self.df_combined_blocked_data)
        self.displayData.displayBlocked.update_table_blocked(self.df_combined_blocked_data)

        self.displayData.displayLost.update_table_lost(self.df_combined_lost_data)

        self.displayData.displayStat.updateGraph(self.df_combined_blocked_data, self.df_combined_lost_data)
