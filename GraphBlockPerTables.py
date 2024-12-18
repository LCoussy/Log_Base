# GraphBlockPerTables.py
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot

class GraphBlockPerTables(BoxLayout):
    def __init__(self, **kwargs):
        super(GraphBlockPerTables, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0
        self.build_ui()

    def build_ui(self):
        # Add a Matplotlib chart
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.set_title('Blocages par table')

        # Create the MatplotFigureSubplot widget
        self.figure_widget = MatplotFigureSubplot()
        self.figure_widget.figure = self.fig

        # Add the widget to the main layout
        self.add_widget(self.figure_widget)

    def updateGraph(self, data):
        """
        Update the graph with new data.

        Args:
            data (pd.DataFrame): The new data to display in the graph.
        """
        self.ax.clear()
        if 'table' in data.columns:
            table_counts = data['table'].value_counts()
            table_counts.plot(kind='bar', ax=self.ax)
            self.ax.set_title('Blocages par table')
            self.ax.set_xlabel('Tables')
            self.ax.set_ylabel('Nombre de blocages')
        else:
            self.ax.set_title('Aucune donnée de blocage par table disponible')
        self.figure_widget.figure.canvas.draw_idle()  # Use draw_idle to update the widget