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
        # Ajouter un graphique Matplotlib
        self.fig, self.ax = plt.subplots(1, 1)
        self.ax.set_title('Blocages par jours')

        # Créer le widget MatplotFigureSubplot
        self.figure_widget = MatplotFigureSubplot()
        self.figure_widget.figure = self.fig
                                
        # Ajouter le widget au layout principal
        self.add_widget(self.figure_widget)

    def updateGraph(self, data):
        """
        Update the graph with new data.

        Args:
            data (pd.DataFrame): The new data to display in the graph.
        """

        self.ax.clear()
        if 'date' in data.columns:
            # Convertir la colonne 'date' en datetime pour faciliter le traitement
            data['date'] = pd.to_datetime(data['date'])

            # Calcul du nombre de semaines entre la date la plus ancienne et la plus récente
            min_date = data['date'].min()
            max_date = data['date'].max()
            num_weeks = round((max_date - min_date).days / 7)

            print(f"Date la plus ancienne : {min_date}")
            print(f"Date la plus récente : {max_date}")
            print(f"Nombre de semaines entre les deux dates : {num_weeks:.2f}")

            print ("////////////////////////")
            print(data['date'])
            
            # Grouper les données par jour et compter les occurrences
            daily_counts = data.groupby(data['date'].dt.date).size()

            # Diviser les nombres par le nombre de semaines
            daily_counts /= num_weeks

            print("----------------------")
            print(daily_counts)

            # Remplacer les index par le jour de la semaine
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

            # Appliquer la traduction
            daily_counts.index = [translation[day] for day in daily_counts.index]

            # Étape 3: Créer un index fixe avec les jours de la semaine en français
            days_of_week_fr = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

            daily_counts = daily_counts.reindex(days_of_week_fr, fill_value=0)

            print("******************************")
            print(daily_counts)

            # Tracer le graphique des blocages par jour
            daily_counts.plot(kind='bar', ax=self.ax)
            self.ax.set_title('Blocages par jour')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Nombre de blocages')
        else:
            self.ax.set_title('Aucune donnée de blocage par jour disponible')
        self.figure_widget.figure.canvas.draw_idle()  # Utiliser draw_idle pour mettre à jour le widget