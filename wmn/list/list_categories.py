import os
from pathlib import Path
import json
from colorama import init, Fore, Style


def print_categories():
    # colorama init
    init()
    current_directory = Path(__file__).resolve().parent

    file_path = current_directory.parent.parent / "data" / "wmn-data.json"

    if not os.path.exists(file_path):
        print(Fore.RED, "error wmn-data.json not found", Style.RESET_ALL)
        exit()

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    categories = {site.get("cat") for site in data.get("sites", [])}
    print("Available categories :")
    for cat in sorted(categories):
        print(cat)
