from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.properties import StringProperty

import os
from processing import process_directory, validate_directory

Window.size = (1000, 600)

class DragDropScreen(Screen):
    path = StringProperty()

    def __init__(self, **kwargs):
        super(DragDropScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='horizontal')
        main_layout.add_widget(self.create_left_layout())
        main_layout.add_widget(self.create_right_layout())
        self.add_widget(main_layout)

    def create_left_layout(self):
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)
        self.drop_label = Label(
            text="Drag and Drop",
            size_hint=(1, 0.2),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.3, None)
        )
        left_layout.add_widget(self.drop_label)
        return left_layout

    def create_right_layout(self):
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)
        float_layout = FloatLayout()
        btn_open = Button(
            text="Open",
            size_hint=(0.15, 0.07),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='18sp'
        )
        btn_open.bind(on_press=self.open_filechooser)
        float_layout.add_widget(btn_open)
        right_layout.add_widget(float_layout)
        return right_layout

    def open_filechooser(self, instance):
        filechooser = FileChooserIconView(path=os.path.expanduser("~"), filters=["*"], dirselect=True)
        select_btn = Button(text="Sélectionner", size_hint=(1, 0.1), font_size='18sp')
        select_btn.bind(on_press=lambda x: self.selected_file_or_dir(filechooser))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        layout.add_widget(select_btn)

        self.popup = Popup(
            title="Sélectionner un fichier ou un dossier",
            content=layout,
            size_hint=(0.9, 0.9)
        )
        self.popup.open()

    def selected_file_or_dir(self, filechooser):
        selection = filechooser.selection
        if selection:
            self.path = selection[0]
            if validate_directory(self.path):
                process_directory(self.path)
                self.update_ui_and_navigate()
            else:
                self.show_error_popup("Veuillez sélectionner un dossier valide.")
        self.popup.dismiss()

    def on_file_drop(self, window, file_path):
        self.path = file_path.decode("utf-8")
        self.drop_label.text = f"{self.path}"
        if validate_directory(self.path):
            process_directory(self.path)
            self.update_ui_and_navigate()
        else:
            self.show_error_popup("Fichier invalide.")

    def update_ui_and_navigate(self):
        display_array_screen = self.manager.get_screen('display_array')
        display_array_screen.log_explorer.update_directory(self.path)
        self.manager.current = 'display_array'

    def show_error_popup(self, message):
        popup = Popup(
            title="Erreur",
            content=Label(text=message, halign='center', valign='middle'),
            size_hint=(0.6, 0.4)
        )
        popup.open()

    def on_enter(self):
        Window.bind(on_dropfile=self.on_file_drop)

    def on_leave(self):
        Window.unbind(on_dropfile=self.on_file_drop)
