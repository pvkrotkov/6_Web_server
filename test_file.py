def read_file(filename):
    with open(f"static/html/{filename}.html", 'r', encoding='UTF-8') as file:
        return file.read()


print(read_file('index'))
