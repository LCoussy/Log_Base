# Display.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.pagelayout import PageLayout
from kivy.uix.screenmanager import Screen
from DisplayArray import DisplayArray
from batchOpen import batchOpen
from DisplayLogTree import LogExplorer
from HandleSwitch import HandleSwitch
from DisplayStat import DisplayStat

class DisplayData(Screen):
    """
    Screen that contains the DisplayArray and manages its layout.
    """

    def __init__(self, fileOrDirectoryPath, **kwargs):
        super(DisplayData, self).__init__(**kwargs)
        self.fileOrDirectoryPath = fileOrDirectoryPath
        self.build_ui()

    def build_ui(self):
        """
        Build the user interface of the Display screen.
        """
        # mainLayout = BoxLayout(orientation='horizontal', padding=0, spacing=0)
        mainLayout = PageLayout()
        statLayout = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=10, spacing=10)
        arrayLayout = BoxLayout(orientation='vertical', size_hint=(1, 1), padding=10, spacing=10)
        # statLayout = PageLayout(size_hint=(1, 1))
        # ArrayLayout = PageLayout(size_hint=(1, 1))

        # Create an instance of DisplayArray
        self.displayArray = DisplayArray()
        self.displayStat = DisplayStat()

        # self.logExplorer = LogExplorer(log_directory=self.fileOrDirectoryPath, on_file_selected=self.on_file_selected)
        # Add the HandleSwitch button to each page
        handleSwitchArray = HandleSwitch(pageLayout=mainLayout)
        handleSwitchStat = HandleSwitch(pageLayout=mainLayout)
        arrayLayout.add_widget(handleSwitchArray)
        statLayout.add_widget(handleSwitchStat)


        statLayout.add_widget(self.displayStat)
        arrayLayout.add_widget(self.displayArray)

        mainLayout.add_widget(statLayout)
        mainLayout.add_widget(arrayLayout)

        self.add_widget(mainLayout)