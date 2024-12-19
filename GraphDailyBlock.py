import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot
import pandas as pd
import FilterGraphDatas


class GraphDailyBlock(BoxLayout):
    def __init__(self, graph_type="BLOCKED", **kwargs):
        """
        Initializes the GraphDailyBlock class.

        Args:
            graph_type (str): The type of graph, either "BLOCKED" or "LOST".
        """
        super(GraphDailyBlock, self).__init__(**kwargs)
        self.graph_type = graph_type.upper()  # BLOCKED or LOST
        self.orientation = 'vertical'
        self.padding = 0
        self.spacing = 0
        self.data = pd.DataFrame()  # Initialize data attribute
        self.build_ui()

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
        self.data = data  # Store the data

        self.ax.clear()
        if 'date' in data.columns:
            # Convert the 'date' column to datetime for easier processing
            data['date'] = pd.to_datetime(data['date'])

            data_filtered = data

            if data_filtered.empty:
                self.ax.set_title('Pas de donnee valide')
                self.figure_widget.figure.canvas.draw_idle()
                return

            # Group the data by day and count the occurrences
            daily_counts = data_filtered.groupby(data_filtered['date'].dt.date).size()

            # Plot the graph
            daily_counts.plot(kind='bar', ax=self.ax)

            # Set graph labels and title
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel(f'Nombre de {"blocages" if self.graph_type == "BLOCKED" else "perdues"}')

            self.ax.tick_params(axis='x', labelrotation=45)

            self.fig.subplots_adjust(bottom=0.3)
        else:
            self.ax.set_title('Pas de date trouvee')

        # Update the graph display
        self.figure_widget.figure.canvas.draw_idle()
