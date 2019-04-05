from kivy.graphics import Color
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class Padding(BoxLayout):

    def __init__(self, widget, x, y, **kwargs):
        super(Padding, self).__init__(**kwargs)
        self.padding = (x, y, x, y)
        self.add_widget(widget)


class LabelWithBackground(Label):

    def on_size(self, *kwargs):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[10, ])
