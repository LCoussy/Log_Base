# DisplayStat.py

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.screenmanager import Screen


class DisplayStat(Screen):
    def __init__(self, **kwargs):

        super(DisplayStat, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):

        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        self.add_widget(main_layout)


