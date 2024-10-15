import MainApp as MApp
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

if __name__ == '__main__':
    MApp.MainApp().run()
