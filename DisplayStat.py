from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
import matplotlib.pyplot as plt
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot

class DisplayStat(Screen):
    def __init__(self, **kwargs):
        super(DisplayStat, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        # Créer le layout principal
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)

        # Ajouter un graphique Matplotlib
        fig, ax = plt.subplots(1, 1)
        ax.plot([0, 1, 2, 3, 4], [1, 2, 8, 9, 4], label='Ligne 1')
        ax.plot([2, 8, 10, 15], [15, 0, 2, 4], label='Ligne 2')
        ax.set_title('Exemple de graphique')
        ax.legend()

        # Créer le widget MatplotFigureSubplot
        figure_widget = MatplotFigureSubplot()
        figure_widget.figure = fig

        # Ajouter le widget au layout principal
        main_layout.add_widget(figure_widget)

        # Ajouter le layout principal à l'écran
        self.add_widget(main_layout)