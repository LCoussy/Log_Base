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

import parser as par
import data_handler as dh

from DisplayLogs import LogExplorer

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

    def build_ui(self):
        """
        Build the user interface of the DisplayArray screen.
        
        It includes a horizontal layout with two sections: a log explorer (on the left) 
        and a scrollable grid (on the right) that will display log data.
        """
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        # Left Layout: LogExplorer (TreeView)
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        # Layout for the title in the right section
        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=10, spacing=10)

        # Right Layout: To display the table of logs
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        # Create an instance of LogExplorer
        self.log_explorer = LogExplorer(
            log_directory="",
            display_array=self
        )
        left_layout.add_widget(self.log_explorer)

        # Title label for the right layout
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

        # Create a ScrollView to contain the GridLayout (for log data)
        scroll_view = ScrollView(size_hint=(1, 0.9))  # Occupies 90% of the right section's height
        self.grid_layout = GridLayout(size_hint_y=None, padding=10, spacing=10, row_force_default=True, row_default_height=40)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))  # Dynamically adjust the grid height

        # Add the grid layout inside the scroll view
        scroll_view.add_widget(self.grid_layout)
        right_layout.add_widget(scroll_view)  # Add the scroll view to the right layout

        # Assemble the main layout
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def updateTable(self, selected_files):
        """
        Update the grid layout with log data from the selected files.

        This method parses the selected log files, processes the data to create 
        a combined DataFrame, and displays it in the grid. The table is updated 
        to remove duplicates and dynamically adjust the number of columns.

        Args:
            selected_files (list of str): List of file paths to be parsed and displayed.
        """
        # Clear existing table content
        self.grid_layout.clear_widgets()
        df_combined = pd.DataFrame()

        # Parse each selected log file and add its data to the combined DataFrame
        for file in selected_files:
            df = dh.createTableBlockedRequest(par.parse_log(file))

            if df is not None and not df.empty:
                df_combined = pd.concat([df_combined, df], ignore_index=True)

        # Remove duplicates and reset the index
        df_combined.drop_duplicates(inplace=True)
        df_combined.reset_index(drop=True, inplace=True)

        # If the combined DataFrame is not empty, populate the grid layout
        if not df_combined.empty:
            self.grid_layout.cols = df_combined.shape[1]  # Set the number of columns
            for header in df_combined.columns:
                # Add column headers to the grid
                self.grid_layout.add_widget(Label(text=header, bold=True))
            for row in df_combined.values:
                for cell in row:
                    # Add each cell's content to the grid
                    self.grid_layout.add_widget(Label(text=str(cell)))
