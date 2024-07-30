from colorama import Fore, Style
import requests
import hashlib
import os

api_url = "https://api.github.com/repos/WebBreacher/WhatsMyName/contents/wmn-data.json"
raw_url = "https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json"
local_file_path = "data/wmn-data.json"


def get_github_file_sha():
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["sha"]


def get_local_file_sha():
    if not os.path.exists(local_file_path):
        return None

    with open(local_file_path, "rb") as f:
        content = f.read()

    size = len(content)
    hasher = hashlib.sha1()
    hasher.update(f"blob {size}\0".encode("utf-8"))
    hasher.update(content)
    return hasher.hexdigest()


def download_file(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, "wb") as file:
        file.write(response.content)


def check_and_update_file():

    if os.path.exists(local_file_path):
        local_sha = get_local_file_sha()
    else:
        local_sha = None

    remote_sha = get_github_file_sha()

    if local_sha != remote_sha:
        download_file(raw_url, local_file_path)
        print(Fore.GREEN, "The local file has been updated.", Style.RESET_ALL)
    else:
        print(Fore.GREEN, "The local file is already up to date.", Style.RESET_ALL)


def check_version_status():
    remote_sha = get_github_file_sha()

    local_sha = get_local_file_sha()

    if local_sha != remote_sha:
        return "out of date"
    else:
        return "up to date"
