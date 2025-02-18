from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.clock import Clock

from threading import Thread
import time

class ParsingThreadedProgressBar(BoxLayout):
  def __init__(self, **kwargs):
    super(ParsingThreadedProgressBar, self).__init__(**kwargs)
    self.orientation = 'vertical'

    self.progress_bar = ProgressBar(max=100)
    self.add_widget(self.progress_bar)

    self.label = Label(text='Progress: 0%')
    self.add_widget(self.label)

    # self.start_button = Button(text='Start')
    # self.start_button.bind(on_press=self.start_thread)
    # self.add_widget(self.start_button)

  def start_thread(self, instance):
    self.progress_bar.value = 0
    self.label.text = 'Progress: 0%'
    self.thread = Thread(target=self.run_task)
    self.thread.start()

  def run_task(self):
    for i in range(101):
      time.sleep(0.1)  # Simulate a task taking time
      Clock.schedule_once(lambda dt, value=i: self.update_progress(value), 0)

  def update_progress(self, value):
    self.progress_bar.value = value
    self.label.text = f'Progress: {value}%'

# class ProgressBarApp(App):
#   def build(self):
#     return ThreadedProgressBar()