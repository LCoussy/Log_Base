from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
import matplotlib.pyplot as plt
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot
from GraphBlockPerTables import GraphBlockPerTables
from GraphDailyBlock import GraphDailyBlock

class DisplayStat(Screen):
    def __init__(self, **kwargs):
        super(DisplayStat, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        # Créer le layout principal
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)

        # Créer un GridLayout pour contenir les graphiques
        # grid_layout = GridLayout(padding=10, spacing=10)
        # grid_layout.bind(minimum_height=grid_layout.setter('height'))  # Bind height to the number of children

        # Ajouter un graphique Matplotlib
        # self.fig, self.ax = plt.subplots(1, 1)
        # self.ax.set_title('Exemple de graphique')

        # # Créer le widget MatplotFigureSubplot
        # self.figure_widget = MatplotFigureSubplot()
        # self.figure_widget.figure = self.fig

        # Ajouter le widget au GridLayout
        # grid_layout.add_widget(self.figure_widget)

        # Ajouter une instance de GraphBlockPerTables
        self.graph_block_per_tables = GraphDailyBlock()
        # grid_layout.add_widget(self.graph_block_per_tables)

        # Ajouter le GridLayout à un ScrollView
        # scroll_view = ScrollView(size_hint=(1, 0.9))
        # scroll_view.add_widget(grid_layout)

        # # Ajouter le ScrollView au layout principal
        # main_layout.add_widget(scroll_view)
        # main_layout.add_widget(self.figure_widget)
        main_layout.add_widget(self.graph_block_per_tables)
        # Ajouter le layout principal à l'écran
        self.add_widget(main_layout)

    def updateGraph(self, data):
        """
        Update the graph with new data.

        Args:
            data (pd.DataFrame): The new data to display in the graph.
        """
        # self.ax.clear()
        # self.ax.plot(data['x'], data['y'], label='Ligne 1')
        # self.ax.set_title('Graphique mis à jour')
        # self.ax.legend()
        # self.figure_widget.figure.canvas.draw_idle()  # Utiliser draw_idle pour mettre à jour le widget

        # Mettre à jour le graphique de GraphBlockPerTables
        self.graph_block_per_tables.updateGraph(data)