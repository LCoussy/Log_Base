from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserIconView
import os
import batchOpen as bo

from DisplayLogs import LogExplorer


class DragDropScreen(Screen):
    path = StringProperty()

    def __init__(self, **kwargs):
        super(DragDropScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='horizontal')

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

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1))

        float_layout = FloatLayout()

        btn_open = Button(
            text="Open",
            size_hint=(0.15, 0.07),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='18sp'
        )
        btn_open.bind(on_press=self.open_filechooser)

        btn_graph = Button(
            text="Graph",
            size_hint=(0.15, 0.07),
            pos_hint={'center_x': -0.2, 'center_y': 0.2},
            font_size='18sp'
        )
        btn_graph.bind(on_press=self.go_to_graph)

        float_layout.add_widget(btn_open)
        float_layout.add_widget(btn_graph)

        right_layout.add_widget(float_layout)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def open_filechooser(self, instance):
        # Appel à la classe de filechooser précédente
        filechooser = FileChooserIconView(path="/home", filters=["*"], dirselect=True)
        select_btn = Button(text="Sélectionner", size_hint=(1, 0.1))
        select_btn.bind(on_press=lambda x: self.selected_file_or_dir(filechooser))

        # Layout pour le filechooser et le bouton
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        layout.add_widget(select_btn)

        # Popup qui affiche la fenêtre de sélection
        self.popup = Popup(
            title="Sélectionner un fichier ou un dossier",
            content=layout,
            size_hint=(0.9, 0.9)
        )
        self.popup.open()

    def selected_file_or_dir(self, filechooser):
        # Récupérer la sélection
        selection = filechooser.selection
        if selection:
            selected_path = selection[0]
            print(f"Sélectionné : {selected_path}")

            # Stocker le chemin sélectionné dans la variable path
            self.path = selected_path

            # Si c'est un dossier
            if os.path.isdir(selected_path):
                print(f"{selected_path} est un dossier.")
                # Appeler bo.batchOpen(selected_path)
                files = bo.batchOpen(selected_path)
                for file in files:
                    print(file)
            else:
                print(f"{selected_path} est un fichier.")

            # Mettre à jour le texte du label avec le chemin sélectionné
            self.drop_label.text = f"Fichier sélectionné : {selected_path}"

            # Fermer la popup
            self.popup.dismiss()

    def on_enter(self):
        Window.bind(on_dropfile=self.on_file_drop)

    def on_leave(self):
        Window.unbind(on_dropfile=self.on_file_drop)

    def on_file_drop(self, window, file_path):
        # Mettre à jour la propriété path lors du drag-and-drop
        self.path = file_path.decode("utf-8")
        self.drop_label.text = f"{self.path}"
        print(f" {self.path}")
        bo.batchOpen(self.path)

    def go_to_graph(self, instance):
        self.manager.current = 'graph'

    # Nouvelle fonction pour renvoyer le path
    def get_path(self):

        return self.path

