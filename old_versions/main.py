import os
import re
import time

BASE_DIR = '../test'
PATTERN = r'\s-.+'
REPLACER = ''


# "Arbeiterfunktion", die einzelnen Pfad durchsucht und Unterordner an recursive_walk zurueckgibt
def process_dir(dir_path):
    print("Processing:", dir_path)
    paths = list()
    for root_path, dirnames, filenames in os.walk(dir_path):
        # Unterordner-Pfade in paths speichern
        for name in dirnames:
            paths.append(name)
        # Dateien bearbeiten
        for name in filenames:
            file_name, file_extension = os.path.splitext(name)
            regex_match = re.search(PATTERN, file_name)
            # Wenn regex das Muster gefunden hat, dann ersetzen und abspeichern
            if regex_match is not None:
                print("Found target:", file_name)
                new_file_name = re.sub(PATTERN, REPLACER, file_name)
                print("New name:", new_file_name)
                # Benutze os.path.join um Dateien an richtigen Ort zu schreiben
                old_file_path = os.path.join(root_path, name)
                new_file_path = os.path.join(root_path, new_file_name + file_extension)
                # Eigentliche Schreibfunktion
                os.rename(old_file_path, new_file_path)
    return recursive_walk(paths)


# Hauptfunktion, die rekursiv aufgerufen wird
def recursive_walk(dir_paths):
    print("Walking:", dir_paths)
    # Falls Parameter nur ein einzelnes Objekt ist, konvertiere zu Liste mit diesem Objekt
    if not isinstance(dir_paths, list):
        dir_paths = [dir_paths]
    # Alle Pfade bearbeiten
    for dir_path in dir_paths:
        process_dir(dir_path)


def main():
    recursive_walk(BASE_DIR)


# Timestamps zum groben Geschwindigkeits-Test
print(time.time())
main()
print(time.time())
