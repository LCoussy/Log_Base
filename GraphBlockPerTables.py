import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot
import pandas as pd


class GraphBlockPerTables(BoxLayout):
    def __init__(self, graph_type="BLOCKED", **kwargs):
        """
        Initializes the GraphBlockPerTables class.

        Args:
            graph_type (str): The type of graph, either "BLOCKED" or "LOST".
        """
        super(GraphBlockPerTables, self).__init__(**kwargs)
        self.graph_type = graph_type.upper()  # BLOCKED or LOST
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0
        self.build_ui()
        self.data = pd.DataFrame()  # Initialize data attribute


    def build_ui(self):
        # Create a Matplotlib figure
        self.fig, self.ax = plt.subplots(1, 1)

        # Create the Matplotlib widget to integrate into Kivy
        self.figure_widget = MatplotFigureSubplot()
        self.figure_widget.figure = self.fig

        # Add the widget to the main layout
        self.add_widget(self.figure_widget)

    def updateGraph(self, data):
        """
        Updates the graph with new data.

        Args:
            data (pd.DataFrame): The new data to display in the graph.
        """
        self.data = data # Store the data

        self.ax.clear()
        #if data is not None and 'table' in data_blocked.columns:
        if 'table' in data.columns:
            data_filtered = data

            if data_filtered.empty:
                self.ax.set_title('Pas de donnee valide')
                self.figure_widget.figure.canvas.draw_idle()
                return

            # Count occurrences of table data
            table_counts = data_filtered['table'].value_counts()
            table_counts.plot(kind='bar', ax=self.ax)

            # Set graph labels and title
            self.ax.set_xlabel('Tables')
            self.ax.set_ylabel(f'Nombre de  {"blocages" if self.graph_type == "BLOCKED" else "perdues"}')

            self.ax.tick_params(axis='x', labelrotation=45)

            self.fig.subplots_adjust(bottom=0.3)
        else:
            self.ax.set_title('No table data available')

        # Update the graph display
        self.figure_widget.figure.canvas.draw_idle()
