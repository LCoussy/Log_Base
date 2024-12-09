# Display.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from DisplayArray import DisplayArray
from batchOpen import batchOpen

class Display(Screen):
    """
    Screen that contains the DisplayArray and manages its layout.
    """

    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        """
        Build the user interface of the Display screen.
        """
        main_layout = BoxLayout(orientation='horizontal', padding=0, spacing=0)
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)

        # Create an instance of DisplayArray
        self.display_array = DisplayArray()
        # self.display_array.updateTable(batchOpen("/home/coussy/log-base/ihm_kivy/log/"))
        right_layout.add_widget(self.display_array)
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)