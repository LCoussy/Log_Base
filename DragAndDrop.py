from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.app import App

import concurrent.futures
import threading
import multiprocessing
import os
import time
from processing import process_directory, validate_directory
import GetContentLog
import gc
import tracemalloc

Window.size = (1000, 600)

class DragDropScreen(Screen):
    path = StringProperty()

    def __init__(self, **kwargs):
        super(DragDropScreen, self).__init__(**kwargs)
        self.parsingProcess = multiprocessing.Process(target=self.process_parsing, daemon=True)
        self.filesList = []
        self.build_ui()
    def build_ui(self):
        mainLayout = BoxLayout(orientation='horizontal')

        mainLayout.add_widget(self.create_left_layout())
        mainLayout.add_widget(self.create_right_layout())
        self.add_widget(mainLayout)

    def process_parsing(self):

        class Loading(BoxLayout):
            loader = Image(source="loading.gif", size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.5})
            self.add_widget(loader)

            loader.opacity = 1  # Affiche la barre de progression

            liste_fichiers = [os.path.join(self.path, file) for file in os.listdir(self.path)]
            chunk_size = 1000

            def chunks(lst, n):
                for i in range(0, len(lst), n):
                    yield lst[i:i + n]

            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                for chunk in chunks(liste_fichiers, chunk_size):
                    # executor.map(self.process_parsing_one_file, chunk)
                    # Libérer la mémoire et vider le cache
                    # tracemalloc.start()
                    # snapshot1 = tracemalloc.take_snapshot()

                    # Process files in the chunk
                    executor.map(self.process_parsing_one_file, chunk)

                    # snapshot2 = tracemalloc.take_snapshot()
                    # top_stats = snapshot2.compare_to(snapshot1, 'lineno')

                    # print("[ Top 10 differences ]")
                    # for stat in top_stats[:10]:
                    #     print(stat)

                    # time.sleep(15)

                    executor.shutdown(wait=True)
                    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
                    gc.collect()

            loader.opacity = 0  # Cache la barre de progression une fois terminé

        class MyApp(App):
            def build(self):
                return Loading()

        MyApp().run()


    def process_parsing_one_file(self, filepath):
        GetContentLog.parse(filepath)

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
                self.update_ui_and_navigate()
            else:
                self.show_error_popup("Veuillez sélectionner un dossier valide.")
        self.popup.dismiss()

    def on_file_drop(self, window, file_path):
        self.path = file_path.decode("utf-8")
        self.dropLabel.text = f"{self.path}"
        if validate_directory(self.path):
            process_directory(self.path)
            self.update_ui_and_navigate()
        else:
            self.show_error_popup("Fichier invalide.")

    def update_ui_and_navigate(self):
        # for file in os.listdir(self.path):
        #     if '/' in self.path:
        #         GetContentLog.parse(self.path + '/' + file)
        #     else :
        #         GetContentLog.parse(self.path + '\\' + file)
        self.parsingProcess.start()
        Screen = self.manager.get_screen('display')
        Screen.logExplorer.update_directory(self.path)
        self.manager.current = 'display'

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
