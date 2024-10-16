from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty  # Import manquant
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.config import Config
import os
import batchOpen as bo

Config.set('input', 'mouse', 'mouse,disable_multitouch')

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



        float_layout.add_widget(btn_open)

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

            # Stocker le chemin sélectionné dans la variable path
            self.path = selected_path

            # Si c'est un dossier, appeler batchOpen pour ouvrir les fichiers
            if os.path.isdir(selected_path):
                files = bo.batchOpen(selected_path)

            # Mettre à jour le texte du label avec le chemin sélectionné
            self.drop_label.text = f"Fichier sélectionné : {selected_path}"

            # Mettre à jour LogExplorer avec le nouveau chemin sélectionné
            log_explorer = self.manager.get_screen('log_screen').children[0]  # LogExplorer est le seul widget de log_screen
            log_explorer.update_directory(selected_path)  # Mise à jour avec le chemin

            # Fermer la popup
            self.popup.dismiss()

            # Bascule vers l'écran des logs après l'ouverture du fichier
            self.manager.current = 'log_screen'

    def on_enter(self):
        Window.bind(on_dropfile=self.on_file_drop)

    def on_leave(self):
        Window.unbind(on_dropfile=self.on_file_drop)

    def on_file_drop(self, window, file_path):
        # Mettre à jour la propriété path lors du drag-and-drop
        self.path = file_path.decode("utf-8")
        self.drop_label.text = f"{self.path}"
        
        # Ouvrir le fichier/dossier avec batchOpen
        bo.batchOpen(self.path)
        
        # Mettre à jour LogExplorer avec le nouveau chemin sélectionné
        log_explorer = self.manager.get_screen('log_screen').children[0]  # LogExplorer est le seul widget de log_screen
        log_explorer.update_directory(self.path)  # Mise à jour avec le chemin
        
        # Bascule vers l'écran des logs après le dépôt du fichier
        self.manager.current = 'log_screen'

    def go_to_graph(self, instance):
        self.manager.current = 'array'

    # Nouvelle fonction pour renvoyer le path
    def get_path(self):
        return self.path
