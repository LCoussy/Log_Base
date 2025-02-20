import multiprocessing.process
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.app import App
from DateRangeSelector import DateSelectionPopup
from datetime import datetime, timedelta

import concurrent.futures
import threading
import multiprocessing
import os
import time
from processing import process_directory, validate_directory
import GetContentLog
import gc
import tracemalloc
import psutil
# import ParsingProgressBar

Window.size = (1000, 600)

class ParsingProgressBar(BoxLayout):
  def __init__(self, **kwargs):
    super(ParsingProgressBar, self).__init__(**kwargs)
    self.orientation = 'vertical'
    self.opacity = 0  # Make the progress bar invisible
    self.progress_bar = ProgressBar(max=100)
    self.add_widget(self.progress_bar)

    self.label = Label(text='Progress: 0%')
    self.add_widget(self.label)

    # self.start_button = Button(text='Start')
    # self.start_button.bind(on_press=self.start_thread)
    # self.add_widget(self.start_button)

  def start_progress(self, _, path):
    self.progress_bar.value = 0
    self.opacity = 1 # Make the progress bar visible
    self.label.text = 'Progress: 0%'
    liste_fichiers = [os.path.join(path, file) for file in os.listdir(path)]
    total_files = len(liste_fichiers)
    self.inc = 0
    self.run_task(liste_fichiers, total_files)

  def run_task(self, liste_fichiers, total_files):
    self.start_time = time.time()
    Clock.schedule_interval(lambda dt : self.update_progress_callback(dt, liste_fichiers, total_files), 0)

  def update_progress_callback(self, dt, liste_fichiers, total_files):

    # print((inc/total_files)*100)
    if self.progress_bar.value < 100:
        GetContentLog.parse(liste_fichiers[self.inc])
        print(self.progress_bar.value)
        self.inc+=1
        self.progress_bar.value = (self.inc/total_files)*100
        self.update_progress(self.progress_bar.value)
    else:
        end_time = time.time()
        print(f"Processing time: {end_time - self.start_time} seconds")
        # Screen = self.manager.get_screen('display')
        # Screen.logExplorer.update_directory(self.path)
        # self.manager.current = 'display'
        return False  # Stop the scheduling

      # self.update_progress(i)

  def update_progress(self, value):
    self.label.text = f'Progress: {value:.2f}%'
    if value == 100:
      self.opacity = 0  # Make the progress bar invisible

#   def run_task(self, liste_fichiers, total_files):

#     def process_parsing_one_file(filepath):
#         # print(f"Processing file: {filepath}")
#         GetContentLog.parse(filepath)

#     def process_parsing(liste_fichiers, total_files):
#         start_time = time.time()
#         # liste_fichiers = [os.path.join(self.path, file) for file in os.listdir(self.path)]
#         # total_files = len(liste_fichiers)
#         inc = 0
#         for file in liste_fichiers:
#             process_parsing_one_file(file)
#             inc += 1
#             print((inc/total_files)*100)
#             Clock.schedule_once(lambda dt, value=(inc/total_files)*100: self.update_progress(value), 0)
#             # self.progressBar.update_progress((inc/total_files)*100)

#         end_time = time.time()
#         print(f"Processing time: {end_time - start_time} seconds")

#     process_parsing(liste_fichiers, total_files)

#   def update_progress(self, value):
#     # print("value",value)
#     # time.sleep(0.1)
#     self.progress_bar.value = value
#     self.label.text = f'Progress: {value}%'
#     if value == 100:
#       self.opacity = 0  # Make the progress bar invisible
class DragDropScreen(Screen):
    path = StringProperty()

    def __init__(self, **kwargs):
        super(DragDropScreen, self).__init__(**kwargs)
        self.progressBar = ParsingProgressBar()

        # self.queue = multiprocessing.Queue()

        # self.parsingProcess = multiprocessing.Process(target=self.process_parsing, args=(self.queue,))
        # self.progressProcess = multiprocessing.Process(target=self.update_progress, args=(self.queue,))
        # self.progressProcess = multiprocessing.Process(target=lambda : self.progressBar.start_thread)
        self.filesList = []
        self.nbFiles = 0
        self.build_ui()

    def build_ui(self):
        self.mainLayout = BoxLayout(orientation='horizontal')

        self.mainLayout.add_widget(self.create_left_layout())
        self.mainLayout.add_widget(self.create_right_layout())
        self.add_widget(self.mainLayout)
        self.add_widget(self.progressBar)

    def process_parsing(self):
        start_time = time.time()
        # Your existing code here
        # Calculate the number of workers based on available memory
        # def calculate_workers():
        #     total_memory = psutil.virtual_memory().total
        #     # Assuming each worker needs approximately 500MB of memory
        #     memory_per_worker = 500 * 1024 * 1024
        #     max_workers = (total_memory // memory_per_worker) - 1  # Reserve one thread for UI
        #     return max(1, min(max_workers, 4))  # Ensure at least 1 worker and at most 4 workers
        liste_fichiers = [os.path.join(self.path, file) for file in os.listdir(self.path)]
        total_files = len(liste_fichiers)
        inc = 0
        self.progressBar.start_progress(None)
        # bar = q.get()
        # bar.start_thread(None)
        for file in liste_fichiers:
            self.process_parsing_one_file(file)
            inc += 1
            # print((inc/total_files)*100)
            Clock.schedule_once(lambda dt, value=(inc/total_files)*100: self.progressBar.update_progress(value), 0.1)
            # self.progressBar.update_progress((inc/total_files)*100)

        # with multiprocessing.Pool(processes=4) as pool:
        #     pool.map_async(self.process_parsing_one_file, liste_fichiers)

        # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        #     futures = {executor.submit(self.process_parsing_one_file, file): file for file in liste_fichiers}
        #     for future in concurrent.futures.as_completed(futures):
        #         file = futures[future]
        #         try:
        #             future.result()
        #         except Exception as exc:
        #             print(f'File {file} generated an exception: {exc}')

        # chunk_size = 1000
        # def chunks(lst, n):
        #     for i in range(0, len(lst), n):
        #         yield lst[i:i + n]

        # num_workers = multiprocessing.cpu_count()-1
        # with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        #     for chunk in chunks(liste_fichiers, chunk_size):
        #         executor.map(self.process_parsing_one_file, chunk)
        #         executor.shutdown(wait=True)
        #         executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_workers)
        #         gc.collect()

        # liste_fichiers = [os.path.join(self.path, file) for file in os.listdir(self.path)]
        # chunk_size = 1000
        # def chunks(lst, n):
        #     for i in range(0, len(lst), n):
        #         yield lst[i:i + n]
        # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        #     for chunk in chunks(liste_fichiers, chunk_size):
        #         executor.map(self.process_parsing_one_file, chunk)
        #         executor.shutdown(wait=True)
        #         executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        #         gc.collect()

        end_time = time.time()
        print(f"Processing time: {end_time - start_time} seconds")

    def process_parsing_one_file(self, filepath):
        # print(f"Processing file: {filepath}")
        GetContentLog.parse(filepath)

    # def update_progress(self, queue):
    #     while True:
    #         processed_files, total_files = queue.get()
    #         progress = (processed_files / total_files) * 100
    #         Clock.schedule_once(lambda dt, value=progress: self.progressBar.update_progress(value), 0)
    #         if processed_files >= total_files:
    #             break


    def show_date_selection(self):
        """
        Ouvre la popup de sélection de date après le drag & drop.
        """
        # Définir une plage de dates fictive (remplace par les vraies dates des fichiers)
        start_date = datetime(2023, 11, 26)  # Remplace 2023 par l'année actuelle si nécessaire
        end_date = datetime(2023, 12, 5)

        # Générer toutes les dates dans cette plage
        available_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        def on_date_chosen(selected_date):
            print(f"Date sélectionnée : {selected_date}")  # Remplace par ton code
            self.update_ui_and_navigate(selected_date)

        popup = DateSelectionPopup(on_date_chosen)
        popup.open()

    def create_left_layout(self):
        leftLayout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)
        self.dropLabel = Label(
            text="Drag and Drop",
            size_hint=(1, 0.2),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.3, None)
        )
        leftLayout.add_widget(self.dropLabel)
        return leftLayout

    def create_right_layout(self):
        rightLayout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)
        floatLayout = FloatLayout()
        btnOpen = Button(
            text="Open",
            size_hint=(0.15, 0.07),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_size='18sp'
        )
        btnOpen.bind(on_press=self.open_filechooser)
        floatLayout.add_widget(btnOpen)
        rightLayout.add_widget(floatLayout)
        return rightLayout

    def open_filechooser(self, instance):
        filechooser = FileChooserIconView(path=os.path.expanduser("~"), filters=["*"], dirselect=True)
        selectBtn = Button(text="Sélectionner", size_hint=(1, 0.1), font_size='18sp')
        selectBtn.bind(on_press=lambda x: self.selected_file_or_dir(filechooser))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        layout.add_widget(selectBtn)

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
                self.show_date_selection()  # Montre la popup de sélection de date
            else:
                self.show_error_popup("Veuillez sélectionner un dossier valide.")
        self.popup.dismiss()


    def on_file_drop(self, window, file_path):
        self.path = file_path.decode("utf-8")
        self.dropLabel.text = f"{self.path}"
        if validate_directory(self.path):
            process_directory(self.path)
            self.show_date_selection()
        else:
            self.show_error_popup("Fichier invalide.")

    def check_progress(self, dt, selected_date=None):
        if self.progressBar.progress_bar.value >= 100:
            self.mainLayout.opacity = 1
            Screen = self.manager.get_screen('display')
            if selected_date:
                if selected_date[1]:
                    date_param = selected_date
                else:
                    date_param = selected_date[0]

                Screen.logExplorer.update_directory(self.path, date_param)

            self.manager.current = 'display'
            return False  # Stop the scheduling
        return True  # Continue scheduling

    def update_ui_and_navigate(self, selected_date=None):
        self.nbFiles = len(os.listdir(self.path))
        self.mainLayout.opacity = 0
        self.progressBar.start_progress(None, self.path)  # Start the progress bar
        Clock.schedule_interval(lambda dt:self.check_progress(dt, selected_date), 0.1)  # Check progress every 0.1 seconds

    # def update_ui_and_navigate(self, selected_date=None):
    #     """
    #     Met à jour l'interface et navigue vers l'affichage des logs.
    #     """
    #     for file in os.listdir(self.path):
    #         file_path = os.path.join(self.path, file)
    #         GetContentLog.parse(file_path)

    #     display_screen = self.manager.get_screen('display')

    #     if selected_date:
    #         if selected_date[1]:
    #             date_param = selected_date
    #         else:
    #             date_param = selected_date[0]

    #         display_screen.logExplorer.update_directory(self.path, date_param)

    #     self.manager.current = 'display'


    def show_error_popup(self, message):

        # Création du layout pour inclure le message et le bouton
        content_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        close_button = Button(text="Fermer", size_hint_y=None, height=40)

        message_label = Label(text=message, halign='center', valign='middle')
        message_label.bind(size=message_label.setter('text_size'))

        popup = Popup(
            title="Erreur",
            content=content_layout,
            size_hint=(0.6, 0.4)
        )

         # Lier le bouton pour fermer la popup
        close_button.bind(on_release=popup.dismiss)

        # Ajouter les éléments au layout
        content_layout.add_widget(message_label)
        content_layout.add_widget(close_button)

        popup.open()

    def on_enter(self):
        Window.bind(on_dropfile=self.on_file_drop)

    def on_leave(self):
        Window.unbind(on_dropfile=self.on_file_drop)
