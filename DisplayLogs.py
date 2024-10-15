from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import os
from datetime import datetime


class LogExplorer(BoxLayout):
    log_directory = StringProperty()
    selected_files = ListProperty()  # Liste pour stocker les chemins des fichiers sélectionnés

    def __init__(self, **kwargs):
        super(LogExplorer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.3, 1)

        # Ajout du ScrollView avec le support de la molette de la souris
        self.scroll_view = ScrollView(do_scroll_y=True, size_hint=(1, 1))
        self.treeview = TreeView(root_options=dict(text="Dossier"), hide_root=True, indent_level=4, size_hint_y=None)
        self.treeview.bind(minimum_height=self.treeview.setter('height'))
        self.scroll_view.add_widget(self.treeview)
        self.add_widget(self.scroll_view)

        # Bind l'événement de la molette de la souris pour le scroll
        Window.bind(on_mouse_scroll=self.on_mouse_scroll)

        if self.log_directory:
            self.populate_treeview(self.log_directory)

    def on_mouse_scroll(self, window, x, y, scroll_x, scroll_y):
        if self.scroll_view:
            self.scroll_view.scroll_y += scroll_y / 10.0

    def populate_treeview(self, log_directory):
        if not os.path.exists(log_directory):
            print(f"Le dossier {log_directory} n'existe pas.")
            return

        # Nettoyer l'arborescence actuelle
        self.treeview.clear_widgets()

        # Ajouter le dossier racine dans l'arborescence
        root_node = self.treeview.add_node(TreeViewLabel(text="Logs", size_hint_y=None, height=25))

        nodes = {}

        for root, dirs, files in os.walk(log_directory):
            if not files:
                continue

            files.sort(key=lambda f: os.path.getmtime(os.path.join(root, f)), reverse=True)

            for file in files:
                file_path = os.path.join(root, file)
                file_date = self.get_file_date(file_path)

                year = str(file_date.year)
                month = file_date.strftime('%B')
                day = str(file_date.day)
                hour = str(file_date.hour) + ":00"

                # Gestion des nœuds année, mois, jour, heure
                year_node = nodes.get(year)
                if not year_node:
                    year_node = self.get_or_create_node(year, parent=root_node)
                    nodes[year] = year_node

                month_key = f"{year}/{month}"
                month_node = nodes.get(month_key)
                if not month_node:
                    month_node = self.get_or_create_node(month, parent=year_node)
                    nodes[month_key] = month_node

                day_key = f"{month_key}/{day}"
                day_node = nodes.get(day_key)
                if not day_node:
                    day_node = self.get_or_create_node(day, parent=month_node)
                    nodes[day_key] = day_node

                hour_key = f"{day_key}/{hour}"
                hour_node = nodes.get(hour_key)
                if not hour_node:
                    hour_node = self.get_or_create_node(hour, parent=day_node)
                    nodes[hour_key] = hour_node

                file_date_time = file_date

                # Formater l'heure et les minutes
                formatted_time = file_date_time.strftime('%H:%M')

                # Ajouter le nœud avec le temps formaté
                file_node = self.treeview.add_node(TreeViewLabel(text=formatted_time + ".txt", size_hint_y=None, height=25),
                                                   parent=hour_node)

                # Ajouter un événement pour sélectionner le fichier
                file_node.bind(on_touch_down=self.on_file_click)

    def get_file_date(self, file_path):
        # Récupérer la date de modification du fichier
        file_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(file_time)

    def get_or_create_node(self, text, parent=None):
        # Vérifier si le nœud existe déjà
        for node in self.treeview.iterate_all_nodes():
            if node.text == text and node.parent == parent:
                return node
        # Créer un nouveau nœud si pas trouvé
        new_node = self.treeview.add_node(TreeViewLabel(text=text, size_hint_y=None, height=25), parent=parent)
        return new_node

    def on_file_click(self, instance, touch):
        # Vérifie si l'élément a bien été cliqué
        if instance.collide_point(*touch.pos):
            # Construire le chemin complet du fichier à partir du texte du nœud
            file_name = instance.text
            file_path = os.path.join(self.log_directory, file_name)

            if os.path.isfile(file_path):
                # Si la touche Ctrl est enfoncée, on ajoute à la sélection multiple
                if 'ctrl' in Window.modifiers:
                    if file_path not in self.selected_files:
                        self.selected_files.append(file_path)
                        instance.color_selected = [.5, .5, .5, 1]
                    else:
                        self.selected_files.remove(file_path)
                        instance.color_selected = [.1, .1, .1, 1]
                else:
                    self.selected_files = [file_path]
                print(f"Fichiers sélectionnés : {self.selected_files}")
