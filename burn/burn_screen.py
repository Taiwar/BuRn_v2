from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from burn.ui_helpers import LabelWithBackground, Padding


# Hauptbildschirm
class BuRnScreen(BoxLayout):

    def __init__(self, switch_dirs, run_process, **kwargs):
        super(BuRnScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = (20, 20, 20, 20)

        # Inputfelder und Labels
        self.pattern_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 1),
            padding=(0, 10, 0, 10)
        )
        self.pattern_box.add_widget(
            Label(
                text='Muster:',
                font_size='20sp',
                size_hint=(.5, 1)
            )
        )
        self.pattern = TextInput(
            multiline=False,
            size_hint=(.5, 1)
        )
        self.pattern_box.add_widget(self.pattern)

        self.replacer_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 1),
            padding=(0, 10, 0, 10)
        )
        self.replacer_box.add_widget(
            Label(
                text='Ersetzen durch:',
                font_size='20sp',
                size_hint=(.5, 1)
            )
        )
        self.replacer = TextInput(
            multiline=False,
            size_hint=(.5, 1)
        )
        self.replacer_box.add_widget(self.replacer)

        # Knoepfe
        self.run_button = Button(text="BuRn!", size_hint=(1, .33))
        self.run_button.bind(on_press=lambda _: run_process(self.pattern, self.replacer))
        self.change_dir_button = Button(text="Ordner ändern", size_hint=(1, .33))
        self.change_dir_button.bind(on_press=switch_dirs)

        ueberschrift = LabelWithBackground(
                text='BuRn',
                size_hint=(1, 1),
                font_size='40sp',
                markup=True,
                bold=True,
                color=(0, 0, 0, 1)
        )
        # Hauptwidget befuellen
        self.add_widget(ueberschrift)
        self.add_widget(self.pattern_box)
        self.add_widget(self.replacer_box)
        self.add_widget(Padding(self.run_button, 200, 0))
        self.add_widget(Padding(self.change_dir_button, 200, 0))
