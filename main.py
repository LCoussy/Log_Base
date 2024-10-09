
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty

import matplotlib.pyplot as plt
import os

import batchOpen as bo

kv = '''
'''


class GraphApp(App):
    path = StringProperty()

    def on_file_drop(self, window, file_path):
        self.path = str(file_path.decode("utf-8"))
        print(file_path.decode("utf-8"))
        print(bo.batchOpen(file_path.decode("utf-8")))

    def build(self):
        Window.bind(on_dropfile=self.on_file_drop)
        Window.size = (800, 600)
        main_layout = BoxLayout(orientation='horizontal')

        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1))  # 30% de la largeur
        left_layout.add_widget(Label(text="Drag and drop", size_hint=(1, 0.1), font_size='20sp'))

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
        title = Label(text="Graphique Matplotlib", size_hint=(1, 0.1), font_size='20sp')
        right_layout.add_widget(title)

        self.create_graph()
        img = Image(source="graph.png")
        right_layout.add_widget(img)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        return  main_layout

    def create_graph(self):
        plt.figure(figsize=(5, 5))
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30], label='Exemple de courbe')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Mon Graphique')
        plt.legend()
        plt.savefig("graph.png")
        plt.close()

    def on_stop(self):
        if os.path.exists("graph.png"):
            os.remove("graph.png")

if __name__ == '__main__':
    GraphApp().run()
