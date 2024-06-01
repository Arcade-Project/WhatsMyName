import os
import json
from colorama import init, Fore, Style


def print_categories():
    # colorama init
    init()
    current_directory = os.path.abspath(os.path.dirname(__file__))
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, "data", "wmn-data.json")

    if not os.path.exists(file_path):
        print(Fore.RED, "error wmn-data.json not found", Style.RESET_ALL)
        exit()

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    categories = {site.get("cat") for site in data.get("sites", [])}
    print("Available categories :")
    for cat in sorted(categories):
        print(cat)
