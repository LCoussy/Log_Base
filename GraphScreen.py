from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen

import matplotlib.pyplot as plt


class GraphScreen(Screen):
    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        left_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=10, spacing=10)

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.7, 1), padding=10, spacing=10)
        grid_layout = GridLayout(cols=2, rows=2, size_hint=(1, 0.9), padding=10, spacing=10)

        title = Label(
            text="Graphique Matplotlib",
            size_hint=(1, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        right_layout.add_widget(up_layout)

        self.graph_images = ['graph1.png', 'graph2.png', 'graph3.png', 'graph4.png']

        for graph in self.graph_images:
            graph_image = Image(
                source=graph,
                allow_stretch=True,
                size_hint=(0.9, 0.9),
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            grid_layout.add_widget(graph_image)

        right_layout.add_widget(grid_layout)

        btn_to_main = Button(
            text="Retour au Menu",
            size_hint=(0.6, None),
            height=50,
            pos_hint={'center_x': 0.5},
            font_size='16sp'
        )
        btn_to_main.bind(on_release=self.go_to_main)
        left_layout.add_widget(btn_to_main)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        self.add_widget(main_layout)

    def create_graphs(self):
        plt.figure(figsize=(5, 5))
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30], label=f'Graph')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Mon Graphique')
        plt.legend()
        filename = f"graph.png"
        plt.savefig(filename)
        plt.close()

    def go_to_main(self, instance):
        self.manager.current = 'drag_drop'
