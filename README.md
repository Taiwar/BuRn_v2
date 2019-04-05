# BuRn_v2 - Bulk Rename

## Starten

Zum starten der Version mit grafischer Oberfläche alle dependencies in der requirements.txt installieren.

z.B. mit `pip install -r requirements.txt`.

Dann Hauptprogramm ausführen mit `python main.py`.

Es sollte eine Ordnerauswahl angezeigt werden, für das Laufwerk auf dem das Programm gestartet wurde, hier dann einen
beliebigen Ordner auswählen, der bearbeitet werden soll.

Danach kann man ein Muster eingeben (in der Form einer RegEx) und mit was Teile von Dateinamen ersetzt werden sollen,
auf welche das Muster zutrifft.

**Testordner** mit beliebiger Verzweigungstiefe und Breite können auch mit den Funktionen in `generate_test_dir.py`
generiert werden.

**Logs** mit Details über einen Durchlauf (durchsuchte Ordner, umbenannte Dateien) werden im bearbeiteten Ordner unter
`/.burn` gespeichert.

## Andere Versionen

Das ursprüngliche single-threaded Script ohne Eingabemöglichkeit (Funktion wird nur über Konstanten gesteuert) liegt
unter `old_versions/main.py`.

Wie der Name schon sagt, ist `old_versions/main_multithreaded.py` das ursprüngliche multi-threaded Script ohne
Eingabemöglichkeit.

Beide diese Versionen brauchen keine externen Bibliotheken.

## Weiteres

Projekt wurde entwickelt und getestet mit Python 3.6.

Projekt wurde geschrieben von **Jonas Müller**.