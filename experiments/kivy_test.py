"""
Hello World

https://kivy.org/doc/stable/guide/basic.html
"""

import kivy
kivy.require('1.11.1')
from kivy.app import App  # noqa
from kivy.uix.label import Label  # noqa


class MyApp(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()
