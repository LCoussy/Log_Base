# DisplayArray.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

import pandas as pd

import parser
import data_handler as dh
import GetContentLog

class DisplayArray(Screen):
    def __init__(self, type, **kwargs):
        super(DisplayArray, self).__init__(**kwargs)
        self.df_combined_blocked = pd.DataFrame()  # Stock datas
        self.df_combined_lost = pd.DataFrame()  # Stock datas
        self.myType = type
        self.sort_ascending = True
        self.current_df = None
        self.build_ui()


    def sort_table(self, column, requestType):
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
            self.updateTableFromCurrentData(requestType)

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

        popup = ModalView(size_hint=(0.9, 0.9), auto_dismiss=True)

        popup.open()
        close_button = Button(
            text="Fermer",
            size_hint_y=None,
            height=30
        )
        close_button.bind(on_release=lambda instance: popup.dismiss())
        
        content_layout.add_widget(close_button)
        popup.add_widget(content_layout)
        popup.open()

    def build_ui(self):
        """
        Build the user interface of the DisplayArray screen.

        It includes a horizontal layout with two sections: a log explorer (on the left)
        and a scrollable grid (on the right) that will display log data.
        """
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)

        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=0, spacing=0)
        down_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=0, spacing=0)


        title = Label(
            text="Tableaux des logs : requetes " + self.myType,
            size_hint=(0.8, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        self.progress_bar = ProgressBar(max=100, size_hint=(1, None), height=20)
        up_layout.add_widget(self.progress_bar)
        self.progress_bar.opacity = 0  # Cachée par défaut

        # Scrollable Array
        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.grid_layout = GridLayout(size_hint_y=None, padding=10, spacing=10, row_force_default=True, row_default_height=40)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        scroll_view.add_widget(self.grid_layout)

        down_layout.add_widget(scroll_view)

        # Assemble the main layout
        main_layout.add_widget(up_layout)
        main_layout.add_widget(down_layout)
        self.add_widget(main_layout)

    def updateTableFromCurrentData(self, requestType):
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
            header_button.bind(on_release=lambda instance, col=header: self.sort_table(col, requestType))
            self.grid_layout.add_widget(header_button)

        self.grid_layout.add_widget(Label(text="segment", bold=True))

        for index, row in df_combined2.iterrows():
            for cell in row:
                self.grid_layout.add_widget(Label(text=str(cell)))

            segment_id = self.current_df.loc[index, "segment_id"]
            view_button = Button(text="Afficher")
            if requestType == "blocked":
                view_button.bind(on_release=lambda instance, sid=segment_id: self.show_segment(self.logsBlocked, sid))
            else:
                view_button.bind(on_release=lambda instance, sid=segment_id: self.show_segment(self.logsLost, sid))
            self.grid_layout.add_widget(view_button)

    def update_table_blocked(self, selected_files, callback=None):
        self.grid_layout.clear_widgets()
        self.df_combined_blocked = pd.DataFrame()
        self.logsBlocked = []
        self.progress_bar.value = 0
        self.progress_bar.opacity = 1  # Affiche la barre de progression

        self.selected_files = selected_files
        self.current_file_index = 0
        self.total_files = len(selected_files)
        self.batch_size = 10  # Nombre de fichiers traités par cycle
        self.callback = callback

        Clock.schedule_once(self.process_next_batch_blocked, 0.1)

    def process_next_batch_blocked(self, dt):
        """
        Traite un lot de fichiers à la fois pour améliorer la vitesse sans bloquer l'UI.
        """
        if self.current_file_index < self.total_files:
            end_index = min(self.current_file_index + self.batch_size, self.total_files)

            for i in range(self.current_file_index, end_index):
                file = self.selected_files[i]
                aLog = GetContentLog.parse(file).get('BLOCKED')
                self.logsBlocked.append(aLog)
                df_blocked = dh.create_table_blocked_request(aLog)

                if df_blocked is not None and not df_blocked.empty:
                    self.df_combined_blocked = pd.concat([self.df_combined_blocked, df_blocked], ignore_index=True)

            if self.logsBlocked:
                df_combined = self.df_combined_blocked

            self.current_file_index = end_index  # Mise à jour de l'index

            # Mise à jour de la barre de progression
            self.progress_bar.value = (self.current_file_index / self.total_files) * 100

            # Continue avec le prochain lot
            Clock.schedule_once(self.process_next_batch_blocked, 0.1)
        else:
            self.progress_bar.opacity = 0  # Cache la barre une fois terminé
            if not self.df_combined_blocked.empty:
                self.df_combined_blocked = self.remove_duplicates(self.df_combined_blocked)
                self.df_combined_blocked.drop_duplicates(inplace=True)
                self.df_combined_blocked.reset_index(drop=True, inplace=True)
                self.current_df = self.df_combined_blocked
                self.updateTableFromCurrentData("blocked")

            if self.callback:
                self.callback(self.df_combined_blocked)

    def update_table_lost(self, selected_files, callback=None):
        self.grid_layout.clear_widgets()
        self.df_combined_lost = pd.DataFrame()
        self.logsLost = []
        self.progress_bar.value = 0
        self.progress_bar.opacity = 1  # Affiche la barre de progression

        self.selected_files = selected_files
        self.current_file_index = 0
        self.total_files = len(selected_files)
        self.batch_size = 10  # Nombre de fichiers traités par cycle (ajuste selon tes besoins)
        self.callback = callback

        Clock.schedule_once(self.process_next_batch_lost, 0.1)

    def process_next_batch_lost(self, dt):
        """
        Traite un lot de fichiers à la fois pour améliorer la vitesse sans bloquer l'UI.
        """
        if self.current_file_index < self.total_files:
            end_index = min(self.current_file_index + self.batch_size, self.total_files)

            for i in range(self.current_file_index, end_index):
                file = self.selected_files[i]
                aLog = GetContentLog.parse(file).get('LOST')
                self.logsLost.append(aLog)
                df_lost = dh.create_table_lost_request(aLog)

                if df_lost is not None and not df_lost.empty:
                    self.df_combined_lost = pd.concat([self.df_combined_lost, df_lost], ignore_index=True)

            self.current_file_index = end_index  # Mise à jour de l'index

            # Mise à jour de la barre de progression
            self.progress_bar.value = (self.current_file_index / self.total_files) * 100

            # Continue avec le prochain lot
            Clock.schedule_once(self.process_next_batch_lost, 0.1)
        else:
            self.progress_bar.opacity = 0  # Cache la barre une fois terminé
            if not self.df_combined_lost.empty:
                self.df_combined_lost = self.remove_duplicates(self.df_combined_lost)
                self.df_combined_lost.drop_duplicates(inplace=True)
                self.df_combined_lost.reset_index(drop=True, inplace=True)
                self.current_df = self.df_combined_lost
                self.updateTableFromCurrentData("lost")

            if self.callback:
                self.callback(self.df_combined_lost)