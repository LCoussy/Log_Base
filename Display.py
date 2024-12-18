# Display.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from DisplayData import DisplayData
from DisplayArray import DisplayArray
from batchOpen import batchOpen
from DisplayLogTree import LogExplorer
from kivy.app import App

class Display(Screen):
    """
    Screen that contains the DisplayArray and manages its layout.
    """

    def __init__(self, fileOrDirectoryPath, **kwargs):
        super(Display, self).__init__(**kwargs)
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

        dataBlocked = self.displayData.displayBlocked.update_table_blocked(selected_files)

        dataLost = self.displayData.displayLost.update_table_lost(selected_files)

        self.displayData.displayStat.updateGraph(dataBlocked)
