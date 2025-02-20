from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from FilterFiles import FilterFiles
from datetime import datetime, timedelta
import re

class LogExplorer(BoxLayout):
    """
    Affiche les logs de la période correspondant aux dates sélectionnées.
    """
    log_directory = StringProperty()
    selected_files = ListProperty()
    start_date = StringProperty() 
    end_date = StringProperty()   
    on_files_selected = ObjectProperty(None)

    def __init__(self, log_directory, on_file_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (1, 1)
        self.filter_files = FilterFiles()
        self.on_file_selected = on_file_selected  

        self.top_layout = BoxLayout(size_hint=(1, 0.1), padding=(10, 10), spacing=10)

        self.prev_button = Button(text="<", size_hint=(None, 1), width=80)
        self.prev_button.bind(on_release=self.prev_week)
        self.top_layout.add_widget(self.prev_button)

        self.subtract_button = Button(text="moins", size_hint=(None, 1), width=80)
        self.subtract_button.bind(on_release=self.subtract_week)
        self.top_layout.add_widget(self.subtract_button)

        self.date_label = Label(text="Sélectionnez une période", size_hint=(0.3, 1), font_size=20, halign='center')
        self.top_layout.add_widget(self.date_label)

        self.add_button = Button(text="plus", size_hint=(None, 1), width=80)
        self.add_button.bind(on_release=self.add_week)
        self.top_layout.add_widget(self.add_button)

        self.next_button = Button(text=">", size_hint=(None, 1), width=80)
        self.next_button.bind(on_release=self.next_week)
        self.top_layout.add_widget(self.next_button)

        self.add_widget(self.top_layout)

        self.no_data_label = Label(text="", size_hint=(1, 0.05), font_size=16)
        self.add_widget(self.no_data_label)

        # Champ de texte pour changer la date
        self.date_input = TextInput(hint_text="Entrez une date (dd/mm/yy)", size_hint=(1, None), height=40)
        self.date_input.bind(on_text_validate=self.update_date)  # Mettre à jour la date sur "Enter"
        self.add_widget(self.date_input)

        self.validate_date_button = Button(text="Valider la date", size_hint=(1, None), height=40)
        self.validate_date_button.bind(on_release=self.update_date)
        self.add_widget(self.validate_date_button)

        if log_directory:
            self.update_directory(log_directory, datetime.today().strftime('%d/%m/%y'))  # Période de la date actuelle

    def update_directory(self, new_directory, selected_start_date):
        """
        Met à jour la liste des logs et vérifie si des logs sont disponibles pour la période sélectionnée.
        """
        self.log_directory = new_directory
        
        # Convertir la date d'entrée pour définir la période
        date_obj = datetime.strptime(selected_start_date, '%d/%m/%y')
        
        start_date = date_obj - timedelta(days=date_obj.weekday())
        end_date = start_date + timedelta(days=6)

        self.start_date = start_date.strftime('%d/%m/%y')
        self.end_date = end_date.strftime('%d/%m/%y')
        
        # Calculer le nombre de semaines
        num_weeks = (end_date - start_date).days // 7 + 1
        
        self.date_label.text = f"Logs de la période : {self.start_date} - {self.end_date} ({num_weeks} semaine(s))"

        # 🔹 Récupération des logs pour la période donnée
        logs = self.get_logs_for_period(new_directory, self.start_date, self.end_date)

        self.no_data_label.text = "" if logs else "Pas de données disponibles"
        
        if hasattr(self, 'on_file_selected') and callable(self.on_file_selected):
            self.on_file_selected(logs)

        self.update_navigation_buttons()

    def get_logs_for_period(self, directory, start_date_str, end_date_str):
        try:
            # Convertir les dates de début et de fin
            start_date = datetime.strptime(start_date_str, '%d/%m/%y')
            end_date = datetime.strptime(end_date_str, '%d/%m/%y')

            # Calculer les semaines qui couvrent cette période
            start_week = start_date - timedelta(days=start_date.weekday())  # Lundi de la semaine de début
            end_week = end_date + timedelta(days=(6 - end_date.weekday()))  # Dimanche de la semaine de fin

            logs = []
            # Récupérer les logs pour la période (potentiellement deux semaines)
            logs += self.filter_files.get_logs_in_date_range(directory, start_week, end_week)

            return logs
        except ValueError as e:
            print(f"Erreur de conversion de date : {e}")
            return []

    def update_date(self, instance=None):
        """Met à jour la période en fonction de la date saisie dans le champ de texte."""
        date_text = self.date_input.text.strip()
        if re.match(r"^\d{2}/\d{2}/\d{2}$", date_text):  # Vérifier le format de la date
            self.update_directory(self.log_directory, date_text)  # Appeler update_directory avec la nouvelle date
            self.date_input.text = ""  # Réinitialiser le champ de texte
        else:
            self.date_input.text = "Format invalide!"  # Message d'erreur si le format est incorrect

    def prev_week(self, instance):
        try:
            start_date = datetime.strptime(self.start_date, '%d/%m/%y')
            end_date = datetime.strptime(self.end_date, '%d/%m/%y')

            new_start_date = start_date - timedelta(weeks=1)
            new_end_date = end_date - timedelta(weeks=1)
            logs = self.get_logs_for_period(self.log_directory, new_start_date.strftime('%d/%m/%y'), new_end_date.strftime('%d/%m/%y'))

            if not logs:
                return  

            self.start_date = new_start_date.strftime('%d/%m/%y')
            self.end_date = new_end_date.strftime('%d/%m/%y')
            num_weeks = (end_date - start_date).days // 7 + 1
        
            self.date_label.text = f"Logs de la période : {self.start_date} - {self.end_date} ({num_weeks} semaine(s))"
            self.no_data_label.text = "" if logs else "Pas de données disponibles"
            if hasattr(self, 'on_file_selected') and callable(self.on_file_selected):
                self.on_file_selected(logs)

            self.update_navigation_buttons()

        except ValueError as e:
            print(f"Erreur de conversion de date : {e}")

    def next_week(self, instance):
        try:
            start_date = datetime.strptime(self.start_date, '%d/%m/%y')
            end_date = datetime.strptime(self.end_date, '%d/%m/%y')

            new_start_date = start_date + timedelta(weeks=1)
            new_end_date = end_date + timedelta(weeks=1)
            logs = self.get_logs_for_period(self.log_directory, new_start_date.strftime('%d/%m/%y'), new_end_date.strftime('%d/%m/%y'))

            if not logs:
                return  

            self.start_date = new_start_date.strftime('%d/%m/%y')
            self.end_date = new_end_date.strftime('%d/%m/%y')
            num_weeks = (end_date - start_date).days // 7 + 1
        
            self.date_label.text = f"Logs de la période : {self.start_date} - {self.end_date} ({num_weeks} semaine(s))"

            self.no_data_label.text = "" if logs else "Pas de données disponibles"
            if hasattr(self, 'on_file_selected') and callable(self.on_file_selected):
                self.on_file_selected(logs)

            self.update_navigation_buttons()

        except ValueError as e:
            print(f"Erreur de conversion de date : {e}")

    def add_week(self, instance):
        try:
            start_date = datetime.strptime(self.start_date, '%d/%m/%y')
            end_date = datetime.strptime(self.end_date, '%d/%m/%y')

            new_end_date = end_date + timedelta(weeks=1)

            logs = self.get_logs_for_period(self.log_directory, start_date.strftime('%d/%m/%y'), new_end_date.strftime('%d/%m/%y'))

            if not logs:
                self.add_button.disabled = True
                return  

            self.end_date = new_end_date.strftime('%d/%m/%y')

            num_weeks = (new_end_date - start_date).days // 7 + 1

            self.date_label.text = f"Logs de la période : {self.start_date} - {self.end_date} ({num_weeks} semaine(s))"
            self.no_data_label.text = "" if logs else "Pas de données disponibles"

            if hasattr(self, 'on_file_selected') and callable(self.on_file_selected):
                self.on_file_selected(logs)

            self.update_navigation_buttons()

        except ValueError as e:
            print(f"Erreur de conversion de date : {e}")

    def subtract_week(self, instance):
        try:
            start_date = datetime.strptime(self.start_date, '%d/%m/%y')
            end_date = datetime.strptime(self.end_date, '%d/%m/%y')

            new_end_date = end_date - timedelta(weeks=1)
            logs = self.get_logs_for_period(self.log_directory, start_date.strftime('%d/%m/%y'), new_end_date.strftime('%d/%m/%y'))

            if not logs:
                return  

            self.end_date = new_end_date.strftime('%d/%m/%y')

            num_weeks = (new_end_date - start_date).days // 7 + 1

            self.date_label.text = f"Logs de la période : {self.start_date} - {self.end_date} ({num_weeks} semaine(s))"
            self.no_data_label.text = "" if logs else "Pas de données disponibles"

            if hasattr(self, 'on_file_selected') and callable(self.on_file_selected):
                self.on_file_selected(logs)

            self.update_navigation_buttons()

        except ValueError as e:
            print(f"Erreur de conversion de date : {e}")

    def update_navigation_buttons(self):
        """Active ou désactive les boutons selon la disponibilité des logs"""
        
        start_date = datetime.strptime(self.start_date, '%d/%m/%y')
        end_date = datetime.strptime(self.end_date, '%d/%m/%y')
        prev_start = datetime.strptime(self.start_date, '%d/%m/%y') - timedelta(weeks=1)
        prev_end = prev_start + timedelta(days=6)
        next_start = datetime.strptime(self.end_date, '%d/%m/%y') + timedelta(days=1)  
        next_end = next_start + timedelta(days=6)  

        has_prev_logs = self.get_logs_for_period(self.log_directory, prev_start.strftime('%d/%m/%y'), prev_end.strftime('%d/%m/%y'))
        has_next_logs = self.get_logs_for_period(self.log_directory, next_start.strftime('%d/%m/%y'), next_end.strftime('%d/%m/%y'))

        self.prev_button.disabled = not has_prev_logs
        self.next_button.disabled = not has_next_logs 

        self.subtract_button.disabled = (start_date == end_date)
        self.add_button.disabled = self.next_button.disabled
