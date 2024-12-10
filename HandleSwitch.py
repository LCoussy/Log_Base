# HandleSwitch.py
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class HandleSwitch(BoxLayout):
    def __init__(self, screenManager, pageList, **kwargs):
        super(HandleSwitch, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = 50

        self.switch_button = Button(text="Switch Screen")
        self.switch_button.bind(on_press=self.switch_screen)
        self.add_widget(self.switch_button)

    def switch_screen(self, instance):
        current_screen = self.screenManager.current
        next_screen = 'stat' if current_screen == 'array' else 'array'
        self.screenManager.current = next_screen
