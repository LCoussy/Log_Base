from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.scrollview import ScrollView
import os
from datetime import datetime

class LogExplorer(BoxLayout):
    log_directory = StringProperty()

    def __init__(self, **kwargs):
        super(LogExplorer, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (0.3, 1)

        scroll_view = ScrollView()
        self.treeview = TreeView(root_options=dict(text="Dossier"), hide_root=False, indent_level=4)
        scroll_view.add_widget(self.treeview)
        self.add_widget(scroll_view)

        if self.log_directory:
            self.populate_treeview(self.log_directory)

    def populate_treeview(self, log_directory):
        if not os.path.exists(log_directory):
            print(f"Le dossier {log_directory} n'existe pas.")
            return

        # Nettoyer l'arborescence actuelle
        self.treeview.clear_widgets()

        # Ajouter le dossier racine dans l'arborescence
        root_node = self.treeview.add_node(TreeViewLabel(text=log_directory))

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

                # Gestion des nœuds année, mois, jour
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

                # Ajouter le fichier sous le jour correspondant
                self.treeview.add_node(TreeViewLabel(text=file), parent=day_node)

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
        new_node = self.treeview.add_node(TreeViewLabel(text=text), parent=parent)
        return new_node

    # Méthode pour mettre à jour le log_directory et actualiser l'affichage
    def update_log_directory(self, new_directory):
        self.log_directory = new_directory
        self.populate_treeview(new_directory)
