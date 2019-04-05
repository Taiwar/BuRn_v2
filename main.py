from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from burn.burn_screen import BuRnScreen
from burn.crawler import start_process
from burn.ui_helpers import Padding

Window.clearcolor = (.15, .15, .15, 1)

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


# Hauptklasse
class BuRn(App):

    # Initialisierung
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = ""
        self.sm = ScreenManager()  # ScreenManager verwaltet Screens und wechselt zwischen ihnen
        self.main_screen = Screen()
        self.browser_screen = Screen()

    def build(self):
        # Datei/Ordner-Auswahl-Widget
        file_chooser = FileChooserListView(size_hint_y=1)
        file_chooser.dirselect = True
        file_chooser.multiselect = False
        file_chooser.filter = ["*.-----"]  # Nonsens-Dateiendung um nur Ordner anzuzeigen
        file_chooser.bind(selection=lambda _, x: self.on_select(file_chooser.selection))
        file_chooser.size_hint_min_y = 400

        # Auswahlknopf
        select_button = Button(text="Auswählen", size_hint=(1, .2))
        select_button.bind(on_release=lambda x: self.on_submit())

        # Container für Knopf und Ordnerauswahl
        container = BoxLayout(orientation="vertical")
        container.add_widget(file_chooser)
        container.add_widget(Padding(select_button, 200, 5))

        # Screens
        self.browser_screen.add_widget(container)
        self.main_screen.add_widget(BuRnScreen(switch_dirs=self.switch_dirs, run_process=self.run_process))

        self.sm.switch_to(self.browser_screen)  # Anfangsbildschirm ist die Ordnerauswahl
        return self.sm  # ScreenManager ist "root" der Oberfläche

    def switch_dirs(self, _):
        self.sm.switch_to(self.browser_screen)

    def run_process(self, pattern, replacer):
        # Wenn Muster nicht nichts ist, Crawler starten
        # TODO: Komischer bug, der endlos-Rekursion hervorruft bei mehreren (verschachtelten?) Aufrufen bei einem Run
        if pattern.text != "":
            # Popup dient als Rueckmeldung, dass Prozess erfolgreich war (callback)
            popup = Popup(title="Erfolg",
                          content=Label(text="Alle Dateien gescannt!"),
                          size=(100, 100),
                          size_hint=(0.3, 0.3))
            start_process(self.path, pattern.text, replacer=replacer.text, callback=popup.open)
        else:
            # Popup um falsche Eingabe zu melden
            popup = Popup(title="Fehlschlag",
                          content=Label(text="Bitte ein gültiges Muster eingeben!"),
                          size=(100, 100),
                          size_hint=(0.3, 0.3))
            popup.open()

    def on_select(self, val):
        # Ordnername speichern wenn nicht nichts
        if val is not None:
            self.path = val[0]

    def on_submit(self):
        # Zu Hauptbildschirm wechseln, wenn Pfad nicht nichts ist
        if self.path != "":
            self.sm.switch_to(self.main_screen)


if __name__ == "__main__":
    BuRn().run()
