# HandleSwitch.py
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class HandleSwitch(BoxLayout):
    def __init__(self, pageLayout, **kwargs):
        super(HandleSwitch, self).__init__(**kwargs)
        self.pageLayout = pageLayout
        self.orientation = 'horizontal'
        self.size_hint = (1, None)
        self.height = 50

        self.switch_button = Button(text="Switch Page")
        self.switch_button.bind(on_press=self.switch_page)
        self.add_widget(self.switch_button)

    def switch_page(self, instance):
        current_page = self.pageLayout.page
        next_page = (current_page + 1) % len(self.pageLayout.children)
        self.pageLayout.page = next_page