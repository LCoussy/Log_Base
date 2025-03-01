from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import re

class DateSelectionPopup(Popup):
    def __init__(self, on_date_selected, **kwargs):
        """
        Initializes the DateRangeSelector instance.

        Args:
            on_date_selected (function): Callback function to be called when a date is selected.
            **kwargs: Additional keyword arguments to be passed to the parent class initializer.

        Attributes:
            on_date_selected (function): Stores the callback function for date selection.
            title (str): Title of the date range selector.
            size_hint (tuple): Size hint for the date range selector.
            start_date_input (TextInput): Input field for the start date.
            end_date_input (TextInput): Input field for the end date.
        """
        super().__init__(**kwargs)
        self.on_date_selected = on_date_selected
        self.title = "Entrer une période (dd/mm/yy)"
        self.size_hint = (0.7, 0.3)

        layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

        date_layout = BoxLayout(orientation="horizontal", spacing=5)

        self.start_date_input = TextInput(hint_text="Ex: 05/12/24", multiline=False)

        separator_label = Label(text="à", size_hint_x=None, width=30) 

        self.end_date_input = TextInput(hint_text="Optionnel", multiline=False)

        date_layout.add_widget(self.start_date_input)
        date_layout.add_widget(separator_label)
        date_layout.add_widget(self.end_date_input)

        validate_button = Button(text="Valider")
        validate_button.bind(on_release=self.validate_date)

        layout.add_widget(date_layout)
        layout.add_widget(validate_button)

        self.add_widget(layout)

    def validate_date(self, instance):
        """
        Validates the date input fields and triggers the date selection callback.

        This method checks if the start and end date inputs match the expected date format (DD/MM/YY).
        If the end date is not provided, it defaults to the start date. Upon successful validation,
        it calls the `on_date_selected` callback with the start and end dates. If the callback's
        instance has a method `on_file_selected`, it retrieves logs for the specified period and
        triggers the `on_file_selected` method with the retrieved logs.

        Args:
            instance: The instance of the widget that triggered this method.

        Returns:
            None
        """
        start_date = self.start_date_input.text.strip()
        end_date = self.end_date_input.text.strip()

        date_pattern = r"^\d{2}/\d{2}/\d{2}$"

        if not re.match(date_pattern, start_date):
            self.start_date_input.text = "Format invalide!"
            return

        if end_date and not re.match(date_pattern, end_date):
            self.end_date_input.text = "Format invalide!"
            return

        if end_date == "":
            end_date = start_date

        self.on_date_selected((start_date, end_date))

        if hasattr(self.on_date_selected, '__self__') and hasattr(self.on_date_selected.__self__, 'on_file_selected'):
            logs = self.on_date_selected.__self__.get_logs_for_period(
                self.on_date_selected.__self__.log_directory, start_date, end_date
            )
            self.on_date_selected.__self__.on_file_selected(logs)

        self.dismiss()
