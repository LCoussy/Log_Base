import MainApp as MApp
import kivy
from kivy.config import Config
import logging
from kivy.core.window import Window

# Définir la taille de la fenêtre
Window.size = (1000, Window.height + 1000) 

Config.set('input', 'mouse', 'mouse,disable_multitouch')
kivy.logger.Logger.setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

if __name__ == '__main__':
    MApp.MainApp().run()
