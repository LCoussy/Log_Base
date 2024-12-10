# Display.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from DisplayArray import DisplayArray
from HandleSwitch import HandleSwitch
from DisplayStat import DisplayStat

class DisplayData(Screen):
    """
    Screen that contains the DisplayArray and manages its layout.
    """

    def __init__(self, **kwargs):
        super(DisplayData, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """
        Build the user interface of the Display screen.
        """
        mainBoxLayout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        # buttonLayout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)
        screenManager = ScreenManager()

        # Create screens for DisplayArray and DisplayStat
        array_screen = Screen(name='array')
        stat_screen = Screen(name='stat')

        # Create instances of DisplayArray and DisplayStat
        self.displayArray = DisplayArray()
        self.displayStat = DisplayStat()

        # Add DisplayArray and DisplayStat to their respective screens
        array_screen.add_widget(self.displayArray)
        stat_screen.add_widget(self.displayStat)

        # Add screens to the ScreenManager
        screenManager.add_widget(array_screen)
        screenManager.add_widget(stat_screen)

        # Add the HandleSwitch button to the button layout
        self.handleSwitch = HandleSwitch(screenManager=screenManager)
        # buttonLayout.add_widget(handleSwitch)

        # Add the button layout and the ScreenManager to the main layout
        # mainBoxLayout.add_widget(buttonLayout)
        mainBoxLayout.add_widget(screenManager)

        self.add_widget(mainBoxLayout)
