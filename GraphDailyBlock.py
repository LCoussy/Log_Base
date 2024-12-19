# GraphDailyBlock.py
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot
import pandas as pd


class GraphDailyBlock(BoxLayout):
    def __init__(self, **kwargs):
        super(GraphDailyBlock, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0
        self.build_ui()

    def build_ui(self):
        # Add a Matplotlib graph
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.set_title('Blocages par jours')

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
        print("Rentrer dans GraphDailyBlocks")


        self.ax.clear()
        if 'date' in data.columns:
            # Convert the 'date' column to datetime to facilitate processing
            data['date'] = pd.to_datetime(data['date'])
            
            # Group the data by day and count the occurrences
            daily_counts = data.groupby(data['date'].dt.date).size()

            # Plot the graph of blocks by day
            daily_counts.plot(kind='bar', ax=self.ax)
            self.ax.set_title('Blocages par jour')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Nombre de blocages')
        else:
            self.ax.set_title('Aucune donnée de blocage par jour disponible')
        self.figure_widget.figure.canvas.draw_idle()  # Utiliser draw_idle pour mettre à jour le widget
