# DisplayData.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import HandleSwitch as hs
from DisplayArray import DisplayArray
from DisplayStat import DisplayStat

class DisplayData(Screen):
    """
    DisplayData is a Kivy Screen class that builds and manages the user interface for displaying data.

    Attributes:
        instance (list): A list containing instances of data to be displayed.
        displayLost (DisplayArray): An instance of DisplayArray for displaying lost requests.
        displayBlocked (DisplayArray): An instance of DisplayArray for displaying blocked requests.
        displayStat (DisplayStat): An instance of DisplayStat for displaying statistics.
        handleSwitchGraph (HandleSwitchGraph): A button for switching to the graph display.
        handleSwitchRequest (HandleSwitchRequest): A button for switching to the request display.

    Methods:
        __init__(**kwargs): Initializes the DisplayData screen and builds the UI.
        build_ui(): Builds the user interface of the Display screen.
    """

    def __init__(self, **kwargs):
        super(DisplayData, self).__init__(**kwargs)
        self.instance = ['']
        self.build_ui()


    def build_ui(self):
        """
        Build the user interface of the Display screen.
        """
        screenManager = ScreenManager()


        mainBoxLayout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        mainBoxLayoutUp = BoxLayout(orientation='horizontal', size_hint=(1, 0.9), padding=10, spacing=10)
        mainBoxLayoutDownButton = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=5, spacing=5)

        # Create instances of DisplayArray and DisplayStat
        self.displayLost = DisplayArray("perdues")
        self.displayBlocked = DisplayArray("bloquees")
        self.displayStat = DisplayStat()

        # Create screens for DisplayArray and DisplayStat
        stat_screen = Screen(name='stat')
        lost_request_screen = Screen(name='lost')
        blocked_request_screen = Screen(name='blocked')

        # Create screens for DisplayArray and DisplayStat

        lost_request_screen.add_widget(self.displayLost)
        blocked_request_screen.add_widget(self.displayBlocked)

        # Add the HandleSwitch button to the button layout
        self.handleSwitchGraph = hs.HandleSwitchGraph(screenManager=screenManager, instance=self.instance)
        self.handleSwitchRequest = hs.HandleSwitchRequest(screenManager=screenManager, instance=self.instance)

        # Ajouter les boutons avec le même size_hint_y pour une hauteur égale
        self.handleSwitchRequest.size_hint_y = 0.8
        self.handleSwitchGraph.size_hint_y = 0.8

        self.handleSwitchRequest.size_hint_x = 0.8
        self.handleSwitchGraph.size_hint_x = 0.8



        mainBoxLayoutDownButton.add_widget(self.handleSwitchRequest)
        mainBoxLayoutDownButton.add_widget(self.handleSwitchGraph)

        stat_screen.add_widget(self.displayStat)

        # Add screens to the ScreenManager
        screenManager.add_widget(lost_request_screen)
        screenManager.add_widget(blocked_request_screen)
        screenManager.add_widget(stat_screen)

        # Add the button layout and the ScreenManager to the main layout
        mainBoxLayoutUp.add_widget(screenManager)
        mainBoxLayout.add_widget(mainBoxLayoutUp)
        mainBoxLayout.add_widget(mainBoxLayoutDownButton)
        self.add_widget(mainBoxLayout)