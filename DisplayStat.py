from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from GraphBlockPerTables import GraphBlockPerTables
from GraphAverageDailyBlock import GraphAverageDailyBlock
from GraphDailyBlock import GraphDailyBlock
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class DisplayStat(Screen):
    def __init__(self, **kwargs):
        super(DisplayStat, self).__init__(**kwargs)
        self.graphs = {}  # Dictionary to store the graph instances
        self.build_ui()


    def build_ui(self):
        # Creat the main layout
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)

        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=0, spacing=0)

        # GridLayout with size_hint_y=None and bind on minimum_height
        grid_layout = GridLayout(cols=2, spacing=10, padding=10, size_hint=(1, None))
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Add main title
        title = Label(
            text="Statistiques :",
            size_hint=(0.8, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)


        self.graphs['daily_blocks'] = self.create_graph_with_title(
            "Blocages par jour", GraphDailyBlock(graph_type="BLOCKED"))
        self.graphs['daily_losses'] = self.create_graph_with_title(
            "Pertes par jour", GraphDailyBlock(graph_type="LOST"))

        self.graphs['average_blocks'] = self.create_graph_with_title(
            "Moyenne des blocages par jour", GraphAverageDailyBlock(graph_type="BLOCKED"))
        self.graphs['average_losses'] = self.create_graph_with_title(
            "Moyenne des pertes par jour", GraphAverageDailyBlock(graph_type="LOST"))

        self.graphs['blocks_per_table'] = self.create_graph_with_title(
            "Blocages par table", GraphBlockPerTables(graph_type="BLOCKED"))


        grid_layout.add_widget(self.graphs['daily_blocks'])
        grid_layout.add_widget(self.graphs['daily_losses'])
        grid_layout.add_widget(self.graphs['average_blocks'])
        grid_layout.add_widget(self.graphs['average_losses'])
        grid_layout.add_widget(self.graphs['blocks_per_table'])


        # add GridLayout to ScrolllView
        scroll_view = ScrollView(size_hint=(1, 0.9))  # Limit the visible size to enable scrolling
        scroll_view.add_widget(grid_layout)

        main_layout.add_widget(up_layout)
        main_layout.add_widget(scroll_view)

        self.add_widget(main_layout)

    def create_graph_with_title(self, title, graph_widget):
        """
        Crée un BoxLayout vertical contenant un titre et un graphique.

        Args:
            title (str): Le titre à afficher au-dessus du graphique.
            graph_widget (Widget): Le widget graphique à inclure.

        Returns:
            BoxLayout: Un BoxLayout contenant le titre et le graphique.
        """
        box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))

        # Ajouter un Label pour le titre
        title_label = Label(
            text=title,
            size_hint_y=None,
            height=30,
            font_size=18,
            bold=True,
            halign="center",
            valign="middle"
        )
        title_label.bind(size=title_label.setter('text_size'))

        # Add graph
        graph_widget.size_hint_y = None
        graph_widget.height = 400
        box.add_widget(title_label)
        box.add_widget(graph_widget)

        # Add button to enlarge graph
        enlarge_button = Button(
            text="Agrandir",
            size_hint_y=None,
            height=30
        )
        enlarge_button.bind(on_release=lambda instance: self.show_popup(type(graph_widget)(), title, graph_widget.data))

        box.add_widget(enlarge_button)
        return box

    def show_popup(self, graph_widget, title, data):
        """
        Affiche un graphique dans une popup.

        Args:
            graph_widget (Widget): Le widget graphique à afficher.
            title (str): Le titre de la popup.
            data (pd.DataFrame): Les données à afficher dans le graphique.
        """
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=title, font_size=20, size_hint_y=None, height=40))
        popup_layout.add_widget(graph_widget)

        # Update the graph with the provided data
        graph_widget.updateGraph(data)


        # Ajouter un bouton pour fermer la popup
        close_button = Button(
            text="Fermer",
            size_hint_y=None,
            height=30
        )
        close_button.bind(on_release=lambda instance: popup.dismiss())
        popup_layout.add_widget(close_button)

        popup = Popup(
            title=title,
            content=popup_layout,
            size_hint=(0.9, 0.9)
        )
        popup.open()

    def updateGraph(self, data_blocked, data_lost):
        """
        Update the graphs with new data.

        Args:
            data (pd.DataFrame): The new data to display in the graphs.
        """
        if not data_blocked.empty:

            # Update daily block graphs
            self.graphs['daily_blocks'].children[1].updateGraph(data_blocked)

            # Update average graphs
            self.graphs['average_blocks'].children[1].updateGraph(data_blocked)

            # Update per table graphs
            self.graphs['blocks_per_table'].children[1].updateGraph(data_blocked)

        if not data_lost.empty:

            self.graphs['daily_losses'].children[1].updateGraph(data_lost)

            self.graphs['average_losses'].children[1].updateGraph(data_lost)
