import MainApp as MApp
import kivy
from kivy.config import Config
import logging

Config.set('input', 'mouse', 'mouse,disable_multitouch')
kivy.logger.Logger.setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

if __name__ == '__main__':
    MApp.MainApp().run()
