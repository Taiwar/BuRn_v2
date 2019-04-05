# Datei lesen und als set zurueckgeben
def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


# Set in Datei schreiben, ein Element = Eine Zeile
def set_to_file(_set, file_name):
    with open(file_name, "w") as f:
        for l in sorted(_set):
            f.write(l+"\n")


# Datei lesen und als set zurueckgeben
def file_to_list(file_name):
    results = list()
    with open(file_name, 'rt') as f:
        for line in f:
            results.append(line.replace('\n', ''))
    return results


# Set in Datei schreiben, ein Element = Eine Zeile
def list_to_file(_list, file_name):
    with open(file_name, "w") as f:
        for l in sorted(_list):
            f.write(l+"\n")


# Datei-Inhalte löschen
def delete_file_contents(path):
    open(path, 'w').close()
