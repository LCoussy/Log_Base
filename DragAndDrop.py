from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty  # Import manquant
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserIconView

import os
import batchOpen as bo

Window.size = (1000, 600)

class DragDropScreen(Screen):
    path = StringProperty()

    def __init__(self, **kwargs):
        super(DragDropScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='horizontal')

        # Left Layout: Drop Label
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

        # Right Layout: Open Button
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

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def open_filechooser(self, instance):
        # Create a FileChooserIconView instance
        filechooser = FileChooserIconView(path=os.path.expanduser("~"), filters=["*"], dirselect=True)

        # Create a 'Select' button
        select_btn = Button(text="Sélectionner", size_hint=(1, 0.1), font_size='18sp')
        select_btn.bind(on_press=lambda x: self.selected_file_or_dir(filechooser))

        # Layout for the filechooser and the button
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        layout.add_widget(select_btn)

        # Popup that displays the filechooser
        self.popup = Popup(
            title="Sélectionner un fichier ou un dossier",
            content=layout,
            size_hint=(0.9, 0.9)
        )
        self.popup.open()

    def selected_file_or_dir(self, filechooser):
        # Retrieve the selection
        selection = filechooser.selection
        if selection:
            selected_path = selection[0]

            # Store the selected path
            self.path = selected_path

            # If it's a directory, call batchOpen to process files
            if os.path.isdir(selected_path):
                files = bo.batchOpen(selected_path)

            # Update the drop_label with the selected path
            self.drop_label.text = f"Fichier sélectionné : {selected_path}"

            # Mettre à jour LogExplorer avec le nouveau chemin sélectionné
            log_explorer = self.manager.get_screen('log_screen').children[0]  # LogExplorer est le seul widget de log_screen
            log_explorer.update_directory(selected_path)  # Mise à jour avec le chemin

            # Close the popup
            self.popup.dismiss()

            # Switch to the DisplayArray screen after opening the file
            self.manager.current = 'display_array'  # Updated screen name

    def on_enter(self):
        # Bind the on_dropfile event when entering the screen
        Window.bind(on_dropfile=self.on_file_drop)

    def on_leave(self):
        # Unbind the on_dropfile event when leaving the screen
        Window.unbind(on_dropfile=self.on_file_drop)

    def on_file_drop(self, window, file_path):
        # Update the path property when a file is dropped
        self.path = file_path.decode("utf-8")
        self.drop_label.text = f"{self.path}"

        # Ouvrir le fichier/dossier avec batchOpen
        bo.batchOpen(self.path)

        display_array_screen = self.manager.get_screen('display_array')
        log_explorer = display_array_screen.log_explorer
        log_explorer.update_directory(self.path)
        self.manager.current = 'display_array'

    def go_to_graph(self, instance):
        # Navigate to the 'array' screen (assuming it's the name for DisplayArray)
        self.manager.current = 'array'

    # New function to return the path
    def get_path(self):
        return self.path
