import os
import re
import time
import datetime
import threading
from queue import Queue
from burn.util import *

NUMBER_OF_THREADS = 4

# Multithread-Warteschlange erstellen
queue = Queue()
# Liste, die Threads haelt, erzeugen
threads = []


# Arbeiter-Klasse, die Grundlage fuer Programm bildet
class Worker:
    queue = set()
    crawled = set()
    log = list()

    # Initialisierung
    def __init__(self, base_dir, work_dir, queue_file, crawled_file, log_file, pattern, replacer):
        self.base_dir = base_dir
        self.work_dir = work_dir
        self.queue_file = queue_file
        self.log_file = log_file
        self.crawled_file = crawled_file
        self.pattern = pattern
        self.replacer = replacer
        self.boot()
        self.log.append(f'# Initialised BuRn')
        self.log.append(f'### Started processing: `{base_dir}`')
        self.log.append(f'### Created working dir: `{work_dir}`')
        self.update_files()
        self.crawl_dir('First worker', base_dir)

    # Vorbereitung fuer Multithreading-Koordination
    def boot(self):
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        if not os.path.isfile(self.queue_file):
            with open(self.queue_file, 'w') as f:
                f.write(self.base_dir)
        if not os.path.isfile(self.crawled_file):
            with open(self.crawled_file, 'w') as f:
                f.write('')
        if not os.path.isfile(self.log_file):
            with open(self.log_file, 'w') as f:
                f.write('')
        Worker.queue = file_to_set(self.queue_file)
        Worker.crawled = file_to_set(self.crawled_file)
        Worker.log = file_to_list(self.log_file)

    # Neue Ordner an Warteschlange haengen
    def add_dirs_to_queue(self, dirs):
        for dir_path in dirs:
            if (dir_path in Worker.queue) or (dir_path in Worker.crawled):
                continue
            Worker.queue.add(dir_path)

    # Textdateien fuer andere Threads mit Daten im Arbeitsspeicher aktualisieren
    def update_files(self):
        set_to_file(Worker.queue, self.queue_file)
        set_to_file(Worker.crawled, self.crawled_file)
        list_to_file(Worker.log, self.log_file)

    # Order-Navigationsfunktion
    def crawl_dir(self, thread_name, dir_path):
        if dir_path not in Worker.crawled:
            print(thread_name, 'now crawling', dir_path)
            print('In Queue:', str(len(Worker.queue)), '| Crawled:', str(len(Worker.crawled)))
            Worker.add_dirs_to_queue(self, Worker.process_dir(self, dir_path))
            if dir_path in Worker.queue:
                Worker.queue.remove(dir_path)
            Worker.crawled.add(dir_path)
            Worker.update_files(self)

    # "Arbeiterfunktion", die einzelnen Pfad durchsucht und Unterordner zurueckgibt
    def process_dir(self, dir_path):
        print("Processing:", dir_path)
        paths = list()
        for root_path, dirnames, filenames in os.walk(dir_path):
            if root_path == self.work_dir or '\.burn' in root_path:
                continue
            self.log.append(f'- Crawling `{root_path}`')
            # Unterordner-Pfade in paths speichern
            for name in dirnames:
                paths.append(name)
            # Dateien bearbeiten
            for name in filenames:
                file_name, file_extension = os.path.splitext(name)
                regex_match = re.search(self.pattern, file_name)
                # Wenn regex das Muster gefunden hat, dann ersetzen und abspeichern
                if regex_match is not None:
                    new_file_name = re.sub(self.pattern, self.replacer, file_name)
                    print("Found target:", file_name, "New name:", new_file_name)
                    # Benutze os.path.join um Dateien an richtigen Ort zu schreiben
                    old_file_path = os.path.join(root_path, name)
                    new_file_path = os.path.join(root_path, new_file_name + file_extension)
                    # Eigentliche Schreibfunktion
                    os.rename(old_file_path, new_file_path)
                    self.log.append(f'- Renamed `{file_name}{file_extension}` to `{new_file_name}{file_extension}`')
        return paths


# Arbeiter erstellen (werden beendet wenn Hauptfunktion endet)
def create_workers(worker):
    # Nur neue Threads starten, wenn es noch nicht genug gibt und Threads zu Liste hinzufuegen
    while len(threads) < NUMBER_OF_THREADS:
        t = threading.Thread(target=work, args=(worker,))
        threads.append(t)
        t.daemon = True
        t.start()


# Ordner aus Warteschlangen-Datei in Warteschlange haengen
def create_jobs(callback, queue_file, crawled_file):
    for dir_path in file_to_set(queue_file):
        queue.put(dir_path)
    queue.join()
    crawl(callback, queue_file, crawled_file)


# Wenn Ordner in der Warteschlange sind, Ordner bearbeiten
# Bildet zusammen mit create_jobs den Rekursiven Aspekt
def crawl(callback, queue_file, crawled_file):
    queued_dirs = file_to_set(queue_file)
    if len(queued_dirs) > 0:
        print(str(len(queued_dirs)), 'dirs in the queue')
        create_jobs(callback, queue_file, crawled_file)
    else:
        # Warteschlange loeschen
        os.remove(queue_file)
        os.remove(crawled_file)
        callback(callback, queue_file)
        # Hier terminiert das Programm


# "Job" fuer jeden Arbeiter
def work(worker):
    while True:
        dir_path = queue.get()
        Worker.crawl_dir(worker, threading.current_thread().name, dir_path)
        queue.task_done()


def start_process(root_dir_path, pattern, replacer='', callback=lambda _: print("Finished!")):
    # Arbeitsdateien festlegen
    work_dir = root_dir_path + '/.burn'
    queue_file = work_dir + '/queue.txt'
    crawled_file = work_dir + '/crawled.txt'
    # Log Datei mit Timestamp im namen erstellen
    timestamp = time.time()
    readable_ts = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H%M%S')
    log_file = work_dir + f'/log.{readable_ts}.md'
    # Arbeiter-Klasse initialisieren
    worker = Worker(
        root_dir_path,
        work_dir,
        queue_file,
        crawled_file,
        log_file,
        re.compile(pattern),
        replacer
    )
    # Einzelne Threads/Arbeiter starten
    create_workers(worker)
    # "Arbeit" starten
    crawl(callback, queue_file, crawled_file)
