# Display.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from DisplayData import DisplayData
from DisplayArray import DisplayArray
from batchOpen import batchOpen
from DisplayLogTree import LogExplorer
from kivy.app import App


# class Display(Screen):
#     """
#     Screen that contains the DisplayArray and manages its layout.
#     """

#     def __init__(self, fileOrDirectoryPath, **kwargs):
#         super(Display, self).__init__(**kwargs)
#         self.fileOrDirectoryPath = fileOrDirectoryPath
#         # self.myType = type
#         self.build_ui()

#     def build_ui(self):
#         """
#         Build the user interface of the Display screen.
#         """
#         # Disposition principale verticale
#         main_layout = BoxLayout(orientation='vertical', padding=0, spacing=10)

#         # Disposition centrale pour le tableau
#         content_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), padding=10, spacing=10)

#         # Création des sous-dispositions
#         left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)
#         right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

#         # Instance de DisplayArray et LogExplorer
#         self.displayArray = DisplayArray(type=self.myType)
#         self.logExplorer = LogExplorer(log_directory=self.fileOrDirectoryPath, on_file_selected=self.on_file_selected)

#         left_layout.add_widget(self.logExplorer)
#         right_layout.add_widget(self.displayArray)

#         content_layout.add_widget(left_layout)
#         content_layout.add_widget(right_layout)

#         # Zone pour le bouton en bas
#         button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)

#         # Ajouter les sections au layout principal
#         main_layout.add_widget(content_layout)
#         main_layout.add_widget(button_layout)

#         self.add_widget(main_layout)

class Display(Screen):
    """
    Screen that contains the DisplayArray and manages its layout.
    """

    def __init__(self, fileOrDirectoryPath, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.fileOrDirectoryPath = fileOrDirectoryPath
        # self.on_file_selected = on_file_selected
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
        # Create an instance of DisplayArray
        # self.displayArray = DisplayArray()
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
        # for file in selected_files:

        #     # df = dh.create_table_blocked_request(parser.parse_log(file))
        #     fileParsedFiltered = dh.filter_request_datafile(GetContentLog.parse(file))
        #     df_lost = dh.create_table_lost_request(dataFiltered.get('LOST'))
        #     if df_lost is not None and not df_lost.empty:
        #         self.df_combined_lost = pd.concat([self.df_combined_lost, df_lost], ignore_index=True)

        dataBlocked = self.displayData.displayBlocked.update_table_blocked(selected_files)

        dataLost = self.displayData.displayLost.update_table_lost(selected_files)
        #self.displayData.displayStat.updateGraph(dataBlocked)
        