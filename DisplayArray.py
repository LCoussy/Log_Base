# DisplayArray.py
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

import pandas as pd

import parser
import data_handler as dh
import GetContentLog

Builder.load_string('''
<MyRecycleViewLost>:
    id: my_recycle_view_lost
    viewclass: 'MyViewClassLost'
    RecycleBoxLayout:
        default_size: None, dp(30)  # Taille par défaut des cellules
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<MyViewClassLost>:
    id: my_view_class_lost
    size_hint_y: 1
    height: self.minimum_height
    Label:
        text: root.date
        size_hint_y: None
        height: self.texture_size[1] + dp(4)  # Ajout d'espace vertical
    Label:
        text: root.user
        size_hint_y: None
        height: self.texture_size[1] + dp(4)  # Ajout d'espace vertical
    Label:
        text: root.poste
        size_hint_y: None
        height: self.texture_size[1] + dp(4)  # Ajout d'espace vertical
    Button:
        text: 'Afficher'
        on_press: root.afficher_button_lost()

<MyRecycleViewBlocked>:
    id: my_recycle_view_blocked
    viewclass: 'MyViewClassBlocked'
    RecycleBoxLayout:
        default_size: None, dp(30)  # Taille par défaut des cellules
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'

<MyViewClassBlocked>:
    id: my_view_class_blocked
    size_hint_y: 1
    height: self.minimum_height
    Label:
        text: root.date
        size_hint_y: None
        height: self.texture_size[1] + dp(4)  # Ajout d'espace vertical
    Label:
        text: root.table
        size_hint_y: None
        height: self.texture_size[1] + dp(4)  # Ajout d'espace vertical
    Label:
        text: root.user
        size_hint_y: None
        height: self.texture_size[1] + dp(4)  # Ajout d'espace vertical
    Label:
        text: root.poste
        size_hint_y: None
        height: self.texture_size[1] + dp(4)  # Ajout d'espace vertical
    Button:
        text: 'Afficher'
        on_press: root.afficher_button_blocked()
''')

class MyViewClassLost(BoxLayout):
    date = StringProperty('')
    user = StringProperty('')
    poste = StringProperty('')
    afficher_button_lost = ObjectProperty(None)

class MyRecycleViewLost(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleViewLost, self).__init__(**kwargs)
        self.data = []  # Génère des nombres de 0 à 49
        # self.data = [{'text': str(x), 'position':"Position"} for x in range(33000)]  # Génère des nombres de 0 à 49

    def update(self, data):
        self.data = data
        self.refresh_from_data()
        # self.ids['afficher_bouton'].disabled = False

class MyViewClassBlocked(BoxLayout):
    date = StringProperty('')
    table = StringProperty('')
    user = StringProperty('')
    poste = StringProperty('')
    afficher_button_blocked = ObjectProperty(None)

class MyRecycleViewBlocked(RecycleView):
    def __init__(self, **kwargs):
        super(MyRecycleViewBlocked, self).__init__(**kwargs)
        self.data = []  # Génère des nombres de 0 à 49
        # print(self._get_viewclass)
        # self.data = [{'text': str(x), 'position':"Position"} for x in range(33000)]  # Génère des nombres de 0 à 49

    def update(self, data):
        self.data = data
        print(data)
        # self.data.afficher_button_blocked.bind(on_release=data)
        self.refresh_from_data()
        # self.ids['afficher_bouton'].disabled = False

class DisplayArray(Screen):
    def __init__(self, type, **kwargs):
        super(DisplayArray, self).__init__(**kwargs)
        self.df_combined_blocked = pd.DataFrame()  # Stock datas
        self.df_combined_lost = pd.DataFrame()  # Stock datas
        self.myType = type
        self.sort_ascending = True
        self.current_df = None
        self.build_ui()



    def clean_text(self,text):
        """
        Remove unwanted characters such as tabs or non-printable characters.
        """
        if not isinstance(text, str):
            return str(text)  # Convert non-strings to strings
        return text.replace('\t', ' ').strip()

    def show_segment(self, logs, segment_id):
        """
        Display the raw content of a log segment in a popup.

        Args:
            logs (list): List of logs parsed from files.
            segment_id (str): The unique ID of the segment to display.
        """


        segment_content = parser.get_segment_by_id(logs, segment_id)
        segment_content = self.clean_text(segment_content)

        content_layout = BoxLayout(orientation='horizontal', padding=(20, 10, 10, 10))
        label = Label(
            text=segment_content,
            halign='left',
            valign='top',
            text_size=(Window.width * 0.85, None)
        )
        label.bind(size=label.setter('text_size'))
        content_layout.add_widget(label)

        popup = ModalView(size_hint=(0.9, 0.9), auto_dismiss=True)

        popup.open()
        close_button = Button(
            text="Fermer",
            size_hint_y=None,
            height=30
        )
        close_button.bind(on_release=lambda instance: popup.dismiss())

        content_layout.add_widget(close_button)
        popup.add_widget(content_layout)
        popup.open()

    def build_ui(self):
        """
        Build the user interface of the DisplayArray screen.

        It includes a horizontal layout with two sections: a log explorer (on the left)
        and a scrollable grid (on the right) that will display log data.
        """
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)

        up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=0, spacing=0)
        down_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=0, spacing=0)
        down_up_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.1), padding=0, spacing=0)
        down_down_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9), padding=0, spacing=0)


        title = Label(
            text="Tableaux des logs : requetes " + self.myType,
            size_hint=(0.8, 1),
            font_size='20sp',
            halign='center',
            valign='middle',
            text_size=(Window.width * 0.7, None)
        )
        up_layout.add_widget(title)

        self.progress_bar = ProgressBar(max=100, size_hint=(1, None), height=20)
        up_layout.add_widget(self.progress_bar)
        self.progress_bar.opacity = 0  # Cachée par défaut

        # Scrollable Array
        # scroll_view = ScrollView(size_hint=(1, 0.9))
        self.grid_layout = GridLayout(size_hint_y=None, padding=10, spacing=10, row_force_default=True, row_default_height=40)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.myRVLost = MyRecycleViewLost()
        # scroll_view.add_widget(self.grid_layout)
        # scroll_view.add_widget(self.grid_layout)

        down_layout.add_widget(down_up_layout)
        down_layout.add_widget(down_down_layout)

        headers = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        headers.add_widget(Label(text="Date", size_hint_y=None))
        headers.add_widget(Label(text="Table", size_hint_y=None))
        headers.add_widget(Label(text="User", size_hint_y=None))
        if self.myType == "bloquees":
            headers.add_widget(Label(text="Poste", size_hint_y=None))
        headers.add_widget(Label(text="Afficher", size_hint_y=None))

        down_up_layout.add_widget(headers)
        if self.myType == "bloquees":
            self.myRVBlocked = MyRecycleViewBlocked()
            down_down_layout.add_widget(self.myRVBlocked)
        else:
            self.myRVLost = MyRecycleViewLost()
            down_down_layout.add_widget(self.myRVLost)

        # down_layout.add_widget(self.myRVLost) if self.myType == "lost" else down_layout.add_widget(self.myRVBlocked)
        # Assemble the main layout
        main_layout.add_widget(up_layout)
        main_layout.add_widget(down_layout)
        self.add_widget(main_layout)

    def update_table_blocked(self, selected_files, callback=None):
        self.grid_layout.clear_widgets()
        self.df_combined_blocked = pd.DataFrame()
        self.logsBlocked = []
        self.progress_bar.value = 0
        self.progress_bar.opacity = 1  # Affiche la barre de progression

        self.selected_files = selected_files
        self.current_file_index = 0
        self.total_files = len(selected_files)
        self.batch_size = 10  # Nombre de fichiers traités par cycle
        self.callback = callback

        Clock.schedule_once(self.process_next_batch_blocked, 0.1)

    def process_next_batch_blocked(self, dt):
        """
        Traite un lot de fichiers à la fois pour améliorer la vitesse sans bloquer l'UI.
        """
        if self.current_file_index < self.total_files:
            end_index = min(self.current_file_index + self.batch_size, self.total_files)
            for i in range(self.current_file_index, end_index):
                file = self.selected_files[i]
                aLog = GetContentLog.read_file_pickle(GetContentLog.getLogcacheFilepath(file)).get('BLOCKED')
                self.logsBlocked.append(aLog)
                df_blocked = dh.create_table_blocked_request(aLog)

                if df_blocked is not None and not df_blocked.empty:
                    self.df_combined_blocked = pd.concat([self.df_combined_blocked, df_blocked], ignore_index=True)

            # if self.logsBlocked:
            #     df_combined = self.df_combined_blocked

            self.current_file_index = end_index  # Mise à jour de l'index

            # Mise à jour de la barre de progression
            self.progress_bar.value = (self.current_file_index / self.total_files) * 100

            # Continue avec le prochain lot
            Clock.schedule_once(self.process_next_batch_blocked, 0.1)
        else:
            self.progress_bar.opacity = 0  # Cache la barre une fois terminé
            if not self.df_combined_blocked.empty:
                self.df_combined_blocked.reset_index(drop=True, inplace=True)
                self.current_df = self.df_combined_blocked
                self.myRVBlocked.update(
                    [
                        {
                            'date': row['date'],
                            'table': row['table'],
                            'user': row['utilisateur'],
                            'poste': row['poste'] if row['poste'] is not None else "",
                            'afficher_button_blocked': lambda sid=row['segment_id']: self.show_segment(self.logsBlocked, sid)
                        }
                        for index, row in self.current_df.iterrows()
                    ]
                )
                # self.updateTableFromCurrentData("blocked")

            if self.callback:
                self.callback(self.df_combined_blocked)

    def update_table_lost(self, selected_files, callback=None):
        self.grid_layout.clear_widgets()
        self.df_combined_lost = pd.DataFrame()
        self.logsLost = []
        self.progress_bar.value = 0
        self.progress_bar.opacity = 1  # Affiche la barre de progression

        self.selected_files = selected_files
        self.current_file_index = 0
        self.total_files = len(selected_files)
        self.batch_size = 10  # Nombre de fichiers traités par cycle (ajuste selon tes besoins)
        self.callback = callback

        Clock.schedule_once(self.process_next_batch_lost, 0.1)


    def process_next_batch_lost(self, dt):
        """
        Traite un lot de fichiers à la fois pour améliorer la vitesse sans bloquer l'UI.
        """
        if self.current_file_index < self.total_files:
            end_index = min(self.current_file_index + self.batch_size, self.total_files)

            for i in range(self.current_file_index, end_index):
                file = self.selected_files[i]
                aLog = GetContentLog.read_file_pickle(GetContentLog.getLogcacheFilepath(file)).get('LOST')
                self.logsLost.append(aLog)
                df_lost = dh.create_table_lost_request(aLog)

                if df_lost is not None and not df_lost.empty:
                    self.df_combined_lost = pd.concat([self.df_combined_lost, df_lost], ignore_index=True)

            self.current_file_index = end_index  # Mise à jour de l'index

            # Mise à jour de la barre de progression
            self.progress_bar.value = (self.current_file_index / self.total_files) * 100

            # Continue avec le prochain lot
            Clock.schedule_once(self.process_next_batch_lost, 0.1)
        else:
            self.progress_bar.opacity = 0  # Cache la barre une fois terminé
            if not self.df_combined_lost.empty:
                self.df_combined_lost.reset_index(drop=True, inplace=True)
                self.current_df = self.df_combined_lost
                # self.updateTableFromCurrentData("lost")
                self.myRVLost.update(
                    [
                        {
                            'date': row['date'],
                            'user': row['utilisateur'],
                            'poste': row['poste'] if row['poste'] is not None else "",
                            'afficher_button_lost': lambda sid=row['segment_id']: self.show_segment(self.logsLost, sid)
                        }
                        for index, row in self.current_df.iterrows()
                    ]
                )

            if self.callback:
                self.callback(self.df_combined_lost)
