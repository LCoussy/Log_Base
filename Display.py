#Display.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from DisplayData import DisplayData
from batchOpen import batchOpen
from DisplayEncadrement import LogExplorer

class Display(Screen):
    """
    Display is a Kivy Screen that represents the main user interface for displaying log data.

    Attributes:
        fileOrDirectoryPath (str): Path to the file or directory containing log data.
        displayData (DisplayData): Widget for displaying data.
        logExplorer (LogExplorer): Widget for exploring log files.
        dataLost (DataFrame or None): DataFrame containing lost data, initialized to None.
        dataBlocked (DataFrame or None): DataFrame containing blocked data, initialized to None.

    Methods:
        __init__(fileOrDirectoryPath, **kwargs):
            Initializes the Display screen with the given file or directory path.
        
        build_ui():
            Builds the user interface of the Display screen.
        
        on_file_selected(selected_files):
            Callback function to handle file selection in LogExplorer.
    """


    def __init__(self, fileOrDirectoryPath, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.fileOrDirectoryPath = fileOrDirectoryPath
        self.build_ui()

    def build_ui(self):
        """
        Build the user interface of the Display screen.
        """
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)  

        header_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2), padding=10, spacing=10)

        self.displayData = DisplayData()

        self.logExplorer = LogExplorer(log_directory=self.fileOrDirectoryPath, on_file_selected=self.on_file_selected)

        header_layout.add_widget(self.logExplorer)
        #header_layout.add_widget(switchGraphButton)

        main_layout.add_widget(header_layout)  
        main_layout.add_widget(self.displayData)  

        self.add_widget(main_layout)

    def on_file_selected(self, selected_files):
        """
        Callback function to handle file selection in LogExplorer.

        Args:
            selected_files (list of str): List of selected file paths.
        """
        self.dataLost = None
        self.dataBlocked = None

        def on_data_lost_ready(df_lost):
            self.dataLost = df_lost
            if self.dataLost is not None and self.dataBlocked is not None:
                self.displayData.displayStat.updateGraph(self.dataBlocked, self.dataLost)

        def on_data_blocked_ready(df_blocked):
            self.dataBlocked = df_blocked
            if self.dataLost is not None and self.dataBlocked is not None:
                self.displayData.displayStat.updateGraph(self.dataBlocked, self.dataLost)

        self.displayData.displayLost.update_table_lost(selected_files, callback=on_data_lost_ready)
        self.displayData.displayBlocked.update_table_blocked(selected_files, callback=on_data_blocked_ready)

