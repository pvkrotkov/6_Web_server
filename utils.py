import yaml


def read_file(filename):
    with open(f"static/html/{filename}", 'r', encoding='UTF-8') as file:
        return file.read()


def read_config() -> dict:
    """Чтение настроек из файла yaml"""
    with open("settings.yaml", "r") as file:
        return yaml.safe_load(file)
