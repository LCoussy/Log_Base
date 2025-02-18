# DisplayData.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import HandleSwitch as hs
from DisplayArray import DisplayArray
from DisplayStat import DisplayStat

class DisplayData(Screen):
    """
    Screen that contains the DisplayArray and manages its layout.
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
        mainBoxLayoutDownButton = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=10, spacing=10)

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

        mainBoxLayoutDownButton.add_widget(self.handleSwitchRequest)

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