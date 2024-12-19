import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot
import pandas as pd


class GraphAverageDailyBlock(BoxLayout):
    def __init__(self, graph_type="BLOCKED", **kwargs):
        """
        Initializes the GraphAverageDailyBlock class.

        Args:
            graph_type (str): The type of graph, either "BLOCKED" or "LOST".
        """
        super(GraphAverageDailyBlock, self).__init__(**kwargs)
        self.graph_type = graph_type.upper()  # BLOCKED or LOST
        self.orientation = 'vertical'
        self.data_blocked = pd.DataFrame()  # Initialize data attribute
        self.data_lost = pd.DataFrame()  # Initialize data attribute
        self.padding = 0
        self.spacing = 0
        self.build_ui()

    def build_ui(self):
        # Create the Matplotlib figure
        self.fig, self.ax = plt.subplots(1, 1)

        # Create the Matplotlib widget to integrate it with Kivy
        self.figure_widget = MatplotFigureSubplot()
        self.figure_widget.figure = self.fig
                                
        # Ajouter le widget au layout principal
        self.add_widget(self.figure_widget)



    def updateGraphBLOCKED(self, data_blocked):
        """
        Updates the graph with new data.

        Args:
            data (pd.DataFrame): The new data to display in the graph.
        """
        self.data_blocked = data_blocked  # Store the data

        self.ax.clear()
        if data_blocked is not None and 'table' in data_blocked.columns:
            # Convert the 'date' column to datetime for easier processing
            data_blocked['date'] = pd.to_datetime(data_blocked['date'])

            data_filtered = data_blocked

            if data_filtered.empty:
                self.ax.set_title('No data available')
                self.figure_widget.figure.canvas.draw_idle()
                return

            # Calculate the number of weeks between the earliest and the most recent date
            min_date = data_filtered['date'].min()
            max_date = data_filtered['date'].max()
            num_weeks = max(1, round((max_date - min_date).days / 7))

            # Group data by day and count occurrences
            daily_counts = data_filtered.groupby(data_filtered['date'].dt.date).size()
            daily_counts /= num_weeks  # Weekly average

            # Translate days of the week
            translation = {
                'Monday': 'Lundi',
                'Tuesday': 'Mardi',
                'Wednesday': 'Mercredi',
                'Thursday': 'Jeudi',
                'Friday': 'Vendredi',
                'Saturday': 'Samedi',
                'Sunday': 'Dimanche'
            }

            # Replace indices with the translated day of the week
            daily_counts.index = [
                pd.Timestamp(date).strftime('%A') for date in daily_counts.index
            ]
            daily_counts.index = [translation[day] for day in daily_counts.index]

            daily_counts = daily_counts.groupby(level=0).sum()

            # Reorder to include all days of the week
            days_of_week = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
            daily_counts = daily_counts.reindex(days_of_week, fill_value=0)

            # Plot the data on the graph
            daily_counts.plot(kind='bar', ax=self.ax)
            self.ax.set_ylabel('Moyenne par jour')

            self.ax.tick_params(axis='x', labelrotation=45)

            self.fig.subplots_adjust(bottom=0.3)
        else:
            self.ax.set_title('No data available')

        # Update the display
        self.figure_widget.figure.canvas.draw_idle()

    def updateGraphLOST(self, data_lost):
        """
        Updates the graph with new data.

        Args:
            data (pd.DataFrame): The new data to display in the graph.
        """
        self.data_lost = data_lost  # Store the data

        self.ax.clear()
        if data_lost is not None and 'table' in data_lost.columns:
            # Convert the 'date' column to datetime for easier processing
            data_lost['date'] = pd.to_datetime(data_lost['date'])

            data_filtered = data_lost

            if data_filtered.empty:
                self.ax.set_title('No data available')
                self.figure_widget.figure.canvas.draw_idle()
                return

            # Calculate the number of weeks between the earliest and the most recent date
            min_date = data_filtered['date'].min()
            max_date = data_filtered['date'].max()
            num_weeks = max(1, round((max_date - min_date).days / 7))

            # Group data by day and count occurrences
            daily_counts = data_filtered.groupby(data_filtered['date'].dt.date).size()
            daily_counts /= num_weeks  # Weekly average

            # Translate days of the week
            translation = {
                'Monday': 'Lundi',
                'Tuesday': 'Mardi',
                'Wednesday': 'Mercredi',
                'Thursday': 'Jeudi',
                'Friday': 'Vendredi',
                'Saturday': 'Samedi',
                'Sunday': 'Dimanche'
            }

            # Replace indices with the translated day of the week
            daily_counts.index = [
                pd.Timestamp(date).strftime('%A') for date in daily_counts.index
            ]
            daily_counts.index = [translation[day] for day in daily_counts.index]

            daily_counts = daily_counts.groupby(level=0).sum()

            # Reorder to include all days of the week
            days_of_week = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
            daily_counts = daily_counts.reindex(days_of_week, fill_value=0)

            # Plot the data on the graph
            daily_counts.plot(kind='bar', ax=self.ax)
            self.ax.set_ylabel('Moyenne par jour')

            self.ax.tick_params(axis='x', labelrotation=45)

            self.fig.subplots_adjust(bottom=0.3)
        else:
            self.ax.set_title('No data available')

        # Update the display
        self.figure_widget.figure.canvas.draw_idle()