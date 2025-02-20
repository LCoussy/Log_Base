# HandleSwitch.py
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class HandleSwitchGraph(BoxLayout):
    def __init__(self, screenManager, instance, **kwargs):
        super(HandleSwitchGraph, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = 50
        self.instance = instance
        self.padding = (0, 28, 0, 0)  

        self.switch_button = Button(text="Données/Statistiques")
        self.switch_button.bind(on_press=lambda e: self.switch_screen(self.instance))
        self.add_widget(self.switch_button)

    def switch_screen(self, instance):
        if self.screenManager.current != 'stat':
            instance[0] = self.screenManager.current
            self.screenManager.current = 'stat'



class HandleSwitchRequest(BoxLayout):
    def __init__(self, screenManager, instance, **kwargs):
        super(HandleSwitchRequest, self).__init__(**kwargs)
        self.screenManager = screenManager
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = 50
        self.instance = instance

        self.switch_button = Button(text="Bloquées/Perdues")
        self.switch_button.bind(on_press=lambda e : self.switch_screen(self.instance))
        self.add_widget(self.switch_button)

    def switch_screen(self, instance):
        current_screen = self.screenManager.current
        if (current_screen == 'stat'):
            next_screen = instance[0]
        else:
            instance[0] = current_screen
            next_screen = 'lost' if current_screen == 'blocked' else 'blocked'

        self.screenManager.current = next_screen