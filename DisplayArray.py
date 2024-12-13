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

    def show_file_content(self, file_path):
        """
        Display the content of a log file in a popup.

        Args:
            file_path (str): Path of the file to be displayed.
        """
        from kivy.uix.popup import Popup
        from kivy.uix.scrollview import ScrollView
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        import os

        try:
            with open(file_path, 'r', encoding='ISO-8859-1') as f:
                file_content = f.read()

            scroll_view = ScrollView(size_hint=(1, 1))

            content_label = Label(
                text=file_content,
                size_hint_y=None,
                text_size=(Window.width * 0.9, None),  
                halign='left', 
                valign='top', 
                width=Window.width * 0.9,
                padding=(Window.width * 0.05, 0), 
            )
            content_label.bind(texture_size=content_label.setter('size')) 

            scroll_view.add_widget(content_label) 

            popup = Popup(
                title=f"Contenu de {os.path.basename(file_path)}",
                content=scroll_view,
                size_hint=(0.9, 0.9),
                auto_dismiss=True
            )
            popup.open()
        except Exception as e:
            error_popup = Popup(
                title="Erreur",
                content=Label(text=f"Erreur en ouvrant le fichier : {str(e)}"),
                size_hint=(0.6, 0.4),
                auto_dismiss=True
            )
            error_popup.open()


            
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
        self.grid_layout.clear_widgets()
        df_combined = pd.DataFrame()

        file_paths = {}  # Dictionnaire pour relier les lignes aux fichiers log

        for file in selected_files:
            parsed_logs = parser.parse_log(file)
            df = dh.create_table_blocked_request(parsed_logs)
            if df is not None and not df.empty:
                df_combined = pd.concat([df_combined, df], ignore_index=True)
                for log in parsed_logs:
                    file_paths[log["id"]] = file
        
        # Remove duplicates based on 'id' and keep the most recent log for each 'id'
        df_combined = self.remove_duplicates(df_combined)  

        # Supprimer les duplicatas supplémentaires
        df_combined.drop_duplicates(inplace=True)
        df_combined.reset_index(drop=True, inplace=True)

        if not df_combined.empty:
            self.grid_layout.cols = df_combined.shape[1] + 1  # Ajouter une colonne pour les boutons
            for header in df_combined.columns:
                self.grid_layout.add_widget(Label(text=header, bold=True))
            self.grid_layout.add_widget(Label(text="Log entiere", bold=True))  # En-tête pour les boutons

            for index, row in df_combined.iterrows():
                for cell in row:
                    self.grid_layout.add_widget(Label(text=str(cell)))

                # Ajouter un bouton pour chaque ligne
                file_path = file_paths.get(row["id"])
                if file_path:
                    view_button = Button(text="Afficher")
                    view_button.bind(on_release=lambda instance, fp=file_path: self.show_file_content(fp))
                    self.grid_layout.add_widget(view_button)
                else:
                    self.grid_layout.add_widget(Label(text="N/A"))
