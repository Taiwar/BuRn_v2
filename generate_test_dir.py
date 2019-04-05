import os
import random

TEST_STRINGS = [
    'asdj - asd [tretrtr]',
    'dsdss - ddwwdd',
    '2331ö223423234',
    '01 - 29012019',
    '[dfdgf]_ddwqd_2',
    'daasdkj (232k)'
    'ötfdfthä'
]

TEST_FORMATS = [
    '.mp3',
    '.flac',
    '.jpg',
    '.docx',
    '.png',
    '.raw',
    '.m4a',
    '.ogg'
]


# Ordner mit pseudo-zufaelligen Testdateien generieren
def generate_random_names(directory, depth, file_width):
    for _ in range(0, depth):
        if not os.path.exists(directory):
            print('Creating test directory', directory)
            os.makedirs(directory)
        for _ in range(0, file_width):
            filename = random.choice(TEST_STRINGS)
            fileformat = random.choice(TEST_FORMATS)
            file = os.path.join(directory, filename + fileformat)
            is_used = os.path.isfile(file)
            while is_used:
                file = os.path.join(directory, filename + '-' + fileformat)
                is_used = os.path.isfile(file)
            with open(file, 'w') as f:
                f.write('')
        directory += '/test'


# Verzweigte Ordnerstruktur mit immer den selben Dateien generieren
def generate_tree(directory, width, depth):
    if depth > 0:
        for j in range(0, width):
            dir_name = directory + '/test' + str(j)
            os.makedirs(dir_name)
            i = 0
            for filename in TEST_STRINGS:
                if not os.path.isfile(dir_name):
                    with open(os.path.join(dir_name, filename + TEST_FORMATS[i]), 'w') as f:
                        f.write('')
                i += 1
            generate_tree(dir_name, width, depth-1)


generate_tree('test', 4, 4)
# generate_random('../test', 3, 4)
