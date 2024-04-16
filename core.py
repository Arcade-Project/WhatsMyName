import os
import sys
import json
import time
import argparse
import requests
import threading
from colorama import init

parser = argparse.ArgumentParser(description="WhatsMyName for ARCADE-DB")
parser.add_argument("username", help="Target Username")
parser.add_argument(
    "category", nargs="?", default="false", help="Filter searches by category"
)
parser.add_argument(
    "--print-all", "-a", action="store_true", help="Print also not found"
)

args = parser.parse_args()

account = args.username
print_all_mode = args.print_all

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}


def requestsCheck(e_string, m_string, formatted_url, semaphore, e_code, m_code, name):
    global found_counter
    global current_state
    global total_url
    global last_print
    try:
        response = session.get(formatted_url, headers=headers, timeout=2)
    except Exception:
        # print(f"{current_state},, update")
        semaphore.release()
        current_state += 1
        return
    else:
        status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")

        if status_code == e_code:
            if e_string in decoded_html:
                found = True
                if m_string in decoded_html:
                    found = False
                if found:
                    print(f"{current_state}, {name}, {formatted_url}, found")
                else:
                    print(f"{current_state}, {name}, {formatted_url}, notfound")

        # else:
        # print(f"{current_state},, update")

    semaphore.release()
    current_state += 1


def main(uri_checks):
    global account
    for site in uri_checks:
        url = site.get("uri_check")
        e_string = site.get("e_string")
        m_string = site.get("m_string")

        e_code = site.get("e_code")
        m_code = site.get("m_code")

        name = site.get("name")

        formatted_url = url.format(account=account)

        semaphore.acquire()
        thread = threading.Thread(
            target=requestsCheck,
            args=(e_string, m_string, formatted_url, semaphore, e_code, m_code, name),
        )
        threads.append(thread)
        thread.start()


# def global variable
last_print = ""
current_state = 0

threads = []
semaphore = threading.Semaphore(30)

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "wmn-data.json")

with open(file_path, encoding="utf-8") as f:
    data = json.load(f)

uri_checks = data.get("sites", [])
if args.category != "false":
    valid_categories = data.get("categories", [])
    if args.category not in valid_categories:
        print("ERROR, invalid category name")
        sys.exit()
    else:
        uri_checks = [site for site in uri_checks if site.get("cat") == args.category]
total_url = len(uri_checks)

# start
start_time = time.time()

# colorama init
init()

if __name__ == "__main__":
    print(f"{total_url},WMN")
    with requests.Session() as session:
        main(uri_checks)

for thread in threads:
    thread.join()

end_time = time.time()
execution_time = end_time - start_time
