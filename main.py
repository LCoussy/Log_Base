import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
import matplotlib.pyplot as plt
import os
import batchOpen as bo

class DragDropScreen(Screen):
    path = StringProperty()

    def __init__(self, **kwargs):
        super(DragDropScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='horizontal')
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        self.drop_label = Label(
            text="Déposez un fichier ici",
            size_hint=(1, 0.2),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.3, None)
        )
        left_layout.add_widget(self.drop_label)

        btn_to_graph = Button(
            text="Aller au Graph",
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        btn_to_graph.bind(on_press=self.go_to_graph)
        left_layout.add_widget(btn_to_graph)

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1))

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def on_enter(self):
        Window.bind(on_dropfile=self.on_file_drop)

    def on_leave(self):
        Window.unbind(on_dropfile=self.on_file_drop)

    def on_file_drop(self, window, file_path):
        self.path = file_path.decode("utf-8")
        self.drop_label.text = f"Fichier déposé: {self.path}"
        print(f"Fichier déposé : {self.path}")
        bo.batchOpen(self.path)
        Clock.schedule_once(self.update_graph_screen, 1)

    def update_graph_screen(self, dt):
        graph_screen = self.manager.get_screen('graph')
        graph_screen.create_graph()

    def go_to_graph(self, instance):
        self.manager.current = 'graph'


class GraphScreen(Screen):
    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(
            text="Graphique Matplotlib",
            size_hint=(1, 0.1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        main_layout.add_widget(title)

        self.graph_image = Image(
            source="graph.png",
            allow_stretch=True,
            size_hint=(1, 0.8)
        )
        main_layout.add_widget(self.graph_image)

        btn_to_main = Button(
            text="Retour au Menu",
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        btn_to_main.bind(on_press=self.go_to_main)
        main_layout.add_widget(btn_to_main)

        self.add_widget(main_layout)

    def create_graph(self):
        plt.figure(figsize=(5, 5))
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30], label='Exemple de courbe')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Mon Graphique')
        plt.legend()
        plt.savefig("graph.png")
        plt.close()
        self.graph_image.source = "graph.png"
        self.graph_image.reload()

    def go_to_main(self, instance):
        self.manager.current = 'drag_drop'


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(DragDropScreen(name='drag_drop'))
        sm.add_widget(GraphScreen(name='graph'))
        sm.get_screen('graph').create_graph()
        return sm

    def on_stop(self):
        if os.path.exists("graph.png"):
            os.remove("graph.png")


if __name__ == '__main__':
    MainApp().run()
