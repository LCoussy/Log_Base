# GraphAverageDailyBlock.py
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot
import pandas as pd


class GraphAverageDailyBlock(BoxLayout):
    def __init__(self, **kwargs):
        super(GraphAverageDailyBlock, self).__init__(**kwargs)
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

        self.ax.clear()
        if 'date' in data.columns:
            # Convert the 'date' column to datetime to facilitate processing
            data['date'] = pd.to_datetime(data['date'])

            # Calculate the number of weeks between the oldest and the most recent date
            min_date = data['date'].min()
            max_date = data['date'].max()
            num_weeks = round((max_date - min_date).days / 7)
            
            # Group the data by day and count the occurrences
            daily_counts = data.groupby(data['date'].dt.date).size()

            # Divide the numbers by the number of weeks
            daily_counts /= num_weeks

            # Replace the indexes with the day of the week
            daily_counts.index = [
                pd.Timestamp(date).strftime('%A') for date in daily_counts.index
            ]

            translation = {
                'Monday': 'Lundi',
                'Tuesday': 'Mardi',
                'Wednesday': 'Mercredi',
                'Thursday': 'Jeudi',
                'Friday': 'Vendredi',
                'Saturday': 'Samedi',
                'Sunday': 'Dimanche'
            }

            # Translate the day
            daily_counts.index = [translation[day] for day in daily_counts.index]

            # Create a fixed index with the days of the week in French
            days_of_week_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

            daily_counts = daily_counts.reindex(days_of_week_fr, fill_value=0)

            # Plot the graph of blocks by day
            daily_counts.plot(kind='bar', ax=self.ax)
            self.ax.set_title('Blocages par jour')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Nombre de blocages')
        else:
            self.ax.set_title('Aucune donnée de blocage par jour disponible')
        self.figure_widget.figure.canvas.draw_idle()  # Use draw_idle to update the widget