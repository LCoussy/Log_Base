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

from datetime import datetime


import pandas as pd

import parser
import data_handler as dh

# from DisplayLogs import LogExplorer


class DisplayArray(Screen):
    """
    Screen that displays a grid of logs and includes a log explorer.

    Attributes:
        log_explorer (LogExplorer): Instance of the log explorer UI component.
        grid_layout (GridLayout): Layout used to display log data in a table format.
    """

    def __init__(self, **kwargs):
        """
        Initialize the DisplayArray screen.

        Args:
            **kwargs: Additional keyword arguments passed to the Screen initializer.
        """

        super(DisplayArray, self).__init__(**kwargs)
        self.build_ui()
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

        popup = Popup(
            title=f"Segment {segment_id}",
            content=Label(text=segment_content, halign='left', valign='top'),
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
            text="Tableaux des logs",
            size_hint=(1, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        # right_layout.add_widget(up_layout)

        # Create a ScrollView to contain the GridLayout
        scroll_view = ScrollView(size_hint=(1, 0.9))  # Make it occupy 90% of the right section's height
        self.grid_layout = GridLayout(size_hint_y=None, padding=10, spacing=10, row_force_default=True, row_default_height=40)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))  # Bind height to the number of children

        scroll_view.add_widget(self.grid_layout)  # Add the grid layout to the scroll view
        # right_layout.add_widget(scroll_view)  # Add the scroll view to the right layout
        down_layout.add_widget(scroll_view)  # Add the scroll view to the right layout

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
        # Ensure 'date' is a datetime object for comparison
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

        # Sort the DataFrame by 'id' and 'date' in descending order (most recent first)
        df_sorted = df.sort_values(by=['id', 'date'], ascending=[True, False])

        # Drop duplicates, keeping the first (most recent) occurrence of each 'id'
        df_unique = df_sorted.drop_duplicates(subset='id', keep='first')

        # Return the cleaned DataFrame
        return df_unique

    def updateTable(self, selected_files):
        """
        Update the grid layout with log data from the selected files.

        Args:
            selected_files (list of str): List of file paths to be parsed and displayed.
        """
        self.grid_layout.clear_widgets()  # Clear existing widgets in the grid layout
        logs = []

        for file in selected_files:
            file_logs = parser.parse_log(file)
            logs.extend(file_logs)

        if logs:
            df_combined = dh.create_table_blocked_request(logs)

            if df_combined is not None and not df_combined.empty:
                # Remove duplicates and reset the index
                df_combined = self.remove_duplicates(df_combined)
                df_combined.drop_duplicates(inplace=True)
                df_combined.reset_index(drop=True, inplace=True)

                # Exclude 'segment_id' and 'id' columns for display purposes
                df_combined2 = df_combined.drop(columns=["segment_id", "id"], errors='ignore')

                # Configure the number of columns in the grid layout
                self.grid_layout.cols = len(df_combined2.columns) + 1  

                # Add headers to the grid
                for header in df_combined2.columns:
                    self.grid_layout.add_widget(Label(text=header, bold=True))

                # Add a header for the "segment" button column
                self.grid_layout.add_widget(Label(text="segment", bold=True))  

                # Add rows of data to the grid
                for index, row in df_combined2.iterrows():
                    for cell in row:
                        self.grid_layout.add_widget(Label(text=str(cell)))  # Display data cells

                    # Add the "Afficher" button for each row
                    segment_id = df_combined.loc[index, "segment_id"]  # Retrieve segment_id from the original DataFrame
                    view_button = Button(text="Afficher")
                    view_button.bind(on_release=lambda instance, sid=segment_id: self.show_segment(logs, sid))
                    self.grid_layout.add_widget(view_button)
