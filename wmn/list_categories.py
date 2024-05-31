import os
import json


def print_categories():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "wmn-data.json")
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    categories = {site.get("cat") for site in data.get("sites", [])}
    for cat in sorted(categories):
        print(cat)
