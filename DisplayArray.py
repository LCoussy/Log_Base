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
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime


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
        # self.handleSwitch = handleSwitch
        self.sort_ascending = True
        self.current_df = None
        self.build_ui()


    def sort_table(self, column):
        """
        Sort the DataFrame based on the selected column and update the grid layout.

        Args:
            column (str): The name of the column to sort by.
        """
        if self.current_df is not None and column in self.current_df.columns:
            if not hasattr(self, 'sort_ascending'):
                self.sort_ascending = True

            if hasattr(self, 'sort_column') and self.sort_column == column:
                self.sort_ascending = not self.sort_ascending
            else:
                self.sort_ascending = True
                self.sort_column = column

            self.current_df.sort_values(
                by=column, ascending=self.sort_ascending, inplace=True
            )
            self.current_df.reset_index(drop=True, inplace=True)
            print("column:", column)
            self.updateTableFromCurrentData()


    def populate_table(self, df_combined):
        """
        Populate the grid layout with data from the DataFrame.

        Args:
            df_combined (pd.DataFrame): The DataFrame containing the log data to display.
        """
        self.grid_layout.clear_widgets()

        df_combined2 = df_combined.drop(columns=["segment_id", "id"], errors='ignore')

        self.grid_layout.cols = len(df_combined2.columns) + 1

        for header in df_combined2.columns:
            header_button = Button(text=header, bold=True)
            header_button.bind(on_release=lambda instance, col=header: self.sort_table(col))
            self.grid_layout.add_widget(header_button)

        self.grid_layout.add_widget(Label(text="segment", bold=True))

        # Add rows of data to the grid
        for index, row in df_combined2.iterrows():
            for cell in row:
                self.grid_layout.add_widget(Label(text=str(cell)))

            # Add the "Afficher" button for each row
            segment_id = df_combined.loc[index, "segment_id"]
            view_button = Button(text="Afficher")
            view_button.bind(on_release=lambda instance, sid=segment_id: self.show_segment(self.current_df.to_dict('records'), sid))
            self.grid_layout.add_widget(view_button)

    def clean_text(self,text):
        """
        Remove unwanted characters such as tabs or non-printable characters.
        """
        if not isinstance(text, str):
            return str(text)  # Convert non-strings to strings
        return text.replace('\t', ' ').strip()

    def show_segment(self, logs, segment_id):
        """
        Display the raw content of a log segment in a popup.

        Args:
            logs (list): List of logs parsed from files.
            segment_id (str): The unique ID of the segment to display.
        """
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label

        segment_content = parser.get_segment_by_id(logs, segment_id)
        segment_content = self.clean_text(segment_content)

        content_layout = BoxLayout(orientation='horizontal', padding=(20, 10, 10, 10))
        label = Label(
            text=segment_content,
            halign='left',
            valign='top',
            text_size=(Window.width * 0.85, None)
        )
        label.bind(size=label.setter('text_size'))
        content_layout.add_widget(label)

        popup = Popup(
            title=f"Segment {segment_id}",
            content=content_layout,
            size_hint=(0.9, 0.9),
            auto_dismiss=True
        )
        popup.open()

    def build_ui(self):
        """
        Build the user interface of the DisplayArray screen.

        It includes a horizontal layout with two sections: a log explorer (on the left)
        and a scrollable grid (on the right) that will display log data.
        """
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)

        # Left Layout: LogExplorer (TreeView)
        # left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)
        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=0, spacing=0)
        down_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=0, spacing=0)

        # right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        # Create an instance of LogExplorer
        # self.log_explorer = LogExplorer(
        #     log_directory="",
        #     display_array=self
        # )
        # left_layout.add_widget(self.log_explorer)

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

        # Assemble the main layout
        # main_layout.add_widget(left_layout)
        # main_layout.add_widget(right_layout)
        main_layout.add_widget(up_layout)
        main_layout.add_widget(down_layout)
        self.add_widget(main_layout)

    def remove_duplicates(self, df):
        """
        Remove duplicate entries based on 'id' and keep only the most recent entry for each 'id'
        (based on the 'date' column).

        Args:
            df (DataFrame): The DataFrame containing the logs.

        Returns:
            DataFrame: A DataFrame with duplicates removed, keeping the most recent entry for each 'id'.
        """
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        df_sorted = df.sort_values(by=['id', 'date'], ascending=[True, False])

        df_unique = df_sorted.drop_duplicates(subset='id', keep='first')

        return df_unique
    def updateTableFromCurrentData(self):
        """
        Update the grid layout with the current DataFrame data.
        This method is used to refresh the table after sorting.
        """
        self.grid_layout.clear_widgets()  
        df_combined2 = self.current_df.drop(columns=["segment_id", "id"], errors='ignore')
        self.grid_layout.cols = len(df_combined2.columns) + 1  

        for header in df_combined2.columns:
            sort_symbol = ""
            if hasattr(self, 'sort_column') and self.sort_column == header:
                sort_symbol = " /\\ " if self.sort_ascending else " \\/ "

            header_button = Button(text=f"{header}{sort_symbol}", bold=True)
            header_button.bind(on_release=lambda instance, col=header: self.sort_table(col))
            self.grid_layout.add_widget(header_button)

        self.grid_layout.add_widget(Label(text="segment", bold=True))  

        for index, row in df_combined2.iterrows():
            for cell in row:
                self.grid_layout.add_widget(Label(text=str(cell)))  

            segment_id = self.current_df.loc[index, "segment_id"]  
            view_button = Button(text="Afficher")
            view_button.bind(on_release=lambda instance, sid=segment_id: self.show_segment(self.logs, sid))
            self.grid_layout.add_widget(view_button)

    def update_table_blocked(self, selected_files):
        self.grid_layout.clear_widgets()
        logs = []
        self.df_combined_blocked = pd.DataFrame()  # Initialise le DataFrame pour les contenus bloqués

        for file in selected_files:
            file_logs = parser.parse_log(file)
            logs.extend(file_logs)

            # Ajout du traitement pour df_blocked
            df_blocked = dh.create_table_blocked_request(GetContentLog.parse(file).get('BLOCKED'))
            if df_blocked is not None and not df_blocked.empty:
                self.df_combined_blocked = pd.concat([self.df_combined_blocked, df_blocked], ignore_index=True)

        if logs:
            df_combined = dh.create_table_blocked_request(logs)

            if df_combined is not None and not df_combined.empty:
                df_combined = self.remove_duplicates(df_combined)
                df_combined.drop_duplicates(inplace=True)
                df_combined.reset_index(drop=True, inplace=True)

                df_combined2 = df_combined.drop(columns=["segment_id", "id"], errors='ignore')

                self.grid_layout.cols = len(df_combined2.columns) + 1  
                self.current_df = df_combined  
                self.logs = logs  

                for header in df_combined2.columns:
                    sort_symbol = ""
                    if hasattr(self, 'sort_column') and self.sort_column == header:
                        sort_symbol = " /\\ " if self.sort_ascending else " \\/ "

                    header_button = Button(text=f"{header}{sort_symbol}", bold=True)
                    header_button.bind(on_release=lambda instance, col=header: self.sort_table(col))
                    self.grid_layout.add_widget(header_button)

                self.grid_layout.add_widget(Label(text="segment", bold=True))  

                for index, row in df_combined2.iterrows():
                    for cell in row:
                        self.grid_layout.add_widget(Label(text=str(cell)))  

                    segment_id = df_combined.loc[index, "segment_id"] 
                    view_button = Button(text="Afficher")
                    view_button.bind(on_release=lambda instance, sid=segment_id: self.show_segment(self.logs, sid))
                    self.grid_layout.add_widget(view_button)
                    
    def update_table_lost(self, selected_files):
        self.grid_layout.clear_widgets()
        logs = []
        self.df_combined_lost = pd.DataFrame()  # Initialise le DataFrame pour les contenus perdus

        for file in selected_files:
            file_logs = parser.parse_log(file)
            logs.extend(file_logs)

            # Ajout du traitement pour df_lost
            df_lost = dh.create_table_lost_request(GetContentLog.parse(file).get('LOST'))
            if df_lost is not None and not df_lost.empty:
                self.df_combined_lost = pd.concat([self.df_combined_lost, df_lost], ignore_index=True)

        if logs:
            df_combined = dh.create_table_lost_request(logs)

            if df_combined is not None and not df_combined.empty:
                df_combined = self.remove_duplicates(df_combined)
                df_combined.drop_duplicates(inplace=True)
                df_combined.reset_index(drop=True, inplace=True)

                df_combined2 = df_combined.drop(columns=["segment_id", "id"], errors='ignore')

                self.grid_layout.cols = len(df_combined2.columns) + 1  
                self.current_df = df_combined  
                self.logs = logs  

                for header in df_combined2.columns:
                    sort_symbol = ""
                    if hasattr(self, 'sort_column') and self.sort_column == header:
                        sort_symbol = " /\\ " if self.sort_ascending else " \\/ "

                    header_button = Button(text=f"{header}{sort_symbol}", bold=True)
                    header_button.bind(on_release=lambda instance, col=header: self.sort_table(col))
                    self.grid_layout.add_widget(header_button)

                self.grid_layout.add_widget(Label(text="segment", bold=True))  

                for index, row in df_combined2.iterrows():
                    for cell in row:
                        self.grid_layout.add_widget(Label(text=str(cell)))  

                    segment_id = df_combined.loc[index, "segment_id"] 
                    view_button = Button(text="Afficher")
                    view_button.bind(on_release=lambda instance, sid=segment_id: self.show_segment(self.logs, sid))
                    self.grid_layout.add_widget(view_button)
