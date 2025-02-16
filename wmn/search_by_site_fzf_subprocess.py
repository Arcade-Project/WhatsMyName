import os
import json
import requests
import subprocess
from pathlib import Path
from colorama import init, Fore, Style


def search_by_site(username):

    from wmn import (
        exec_concurrent_uri_checks,
        print_header_and_informations,
        set_total_url,
    )
    # colorama init
    init()
    current_directory = Path(__file__).resolve().parent

    file_path = current_directory.parent / "data" / "wmn-data.json"

    if not os.path.exists(file_path):
        print(Fore.RED, "error wmn-data.json not found", Style.RESET_ALL)
        exit()

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    sites_name = {site.get("name") for site in data.get("sites", [])}

    sorted_sites = sorted(sites_name)

    sites_str = "\n".join(sorted_sites)

    process = subprocess.Popen(
        ['fzf'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    selected_site, _ = process.communicate(input=sites_str)

    if selected_site:

        uri_checks = [site for site in data["sites"]
                      if site["name"] == selected_site.strip()]

        set_total_url(len(uri_checks))
        print_header_and_informations()

        with requests.Session() as session:
            exec_concurrent_uri_checks(uri_checks, username, session)
        return
    else:
        print(Fore.RED, "error no site selected", Style.RESET_ALL)
        return
