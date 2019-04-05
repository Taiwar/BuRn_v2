import os
import re
import threading
from queue import Queue
from burn.util import *
import time

# Konstanten
WORK_DIR = '../tmp'
QUEUE_FILE = os.path.join(WORK_DIR + '/queue.txt')
CRAWLED_FILE = os.path.join(WORK_DIR + '/crawled.txt')
NUMBER_OF_THREADS = 4

# Vom Nutzer einstellbare Werte
# Todo: Eingabemoeglichkeit
BASE_DIR = '../test'
PATTERN = r'\s-.+'
REPLACER = ''

# Multithread-Warteschlange erstellen
queue = Queue()


# Arbeiter-Klasse, die Grundlage fuer Programm bildet
class Worker:
    queue = set()
    crawled = set()

    # Initialisierung
    def __init__(self):
        self.boot()
        self.crawl_dir('First worker', BASE_DIR)

    # Vorbereitung fuer multithreading Koordination
    @staticmethod
    def boot():
        if not os.path.exists(WORK_DIR):
            print('Creating working directory', WORK_DIR)
            os.makedirs(WORK_DIR)
        if not os.path.isfile(QUEUE_FILE):
            with open(QUEUE_FILE, 'w') as f:
                f.write(BASE_DIR)
        if not os.path.isfile(CRAWLED_FILE):
            with open(CRAWLED_FILE, 'w') as f:
                f.write('')
        Worker.queue = file_to_set(QUEUE_FILE)
        Worker.crawled = file_to_set(CRAWLED_FILE)

    # Neue Ordner an Warteschlange haengen
    @staticmethod
    def add_dirs_to_queue(dirs):
        for dir_path in dirs:
            if (dir_path in Worker.queue) or (dir_path in Worker.crawled):
                continue
            Worker.queue.add(dir_path)

    # Textdateien fuer andere Threads mit Daten im Arbeitsspeicher aktualisieren
    @staticmethod
    def update_files():
        set_to_file(Worker.queue, QUEUE_FILE)
        set_to_file(Worker.crawled, CRAWLED_FILE)

    # Order-Navigationsfunktion
    @staticmethod
    def crawl_dir(thread_name, dir_path):
        if dir_path not in Worker.crawled:
            print(thread_name, 'now crawling', dir_path)
            print('In Queue:', str(len(Worker.queue)), '| Crawled:', str(len(Worker.crawled)))
            Worker.add_dirs_to_queue(Worker.process_dir(dir_path))
            if dir_path in Worker.queue:
                Worker.queue.remove(dir_path)
            Worker.crawled.add(dir_path)
            Worker.update_files()

    # "Arbeiterfunktion", die einzelnen Pfad durchsucht und Unterordner zurueckgibt
    @staticmethod
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
        return paths


# Arbeiter erstellen (werden beendet wenn Hauptfunktion endet)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Ordner aus Warteschlangen-Datei in Warteschlange haengen
def create_jobs():
    for dir_path in file_to_set(QUEUE_FILE):
        queue.put(dir_path)
    queue.join()
    crawl()


# Wenn Ordner in der Warteschlange sind, Ordner bearbeiten
# Bildet zusammen mit create_jobs den Rekursiven Aspekt
def crawl():
    queued_dirs = file_to_set(QUEUE_FILE)
    if len(queued_dirs) > 0:
        print(str(len(queued_dirs)), ' dirs in the queue')
        create_jobs()
    else:
        # delete_file_contents(CRAWLED_FILE)
        print("Finished!")
        print(time.time())
        # Hier terminiert das Programm


# "Job" fuer jeden Arbeiter
def work():
    while True:
        dir_path = queue.get()
        Worker.crawl_dir(threading.current_thread().name, dir_path)
        queue.task_done()


# Timestamps zum groben Geschwindigkeits-Test
print(time.time())
# Arbeiter-Klasse initialisieren
Worker()
# Einzelne Threads/Arbeiter starten
create_workers()
# "Arbeit" starten
crawl()
