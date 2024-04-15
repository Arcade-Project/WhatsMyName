import os
import json
import time
import argparse
import requests
import threading
from colorama import init, Back, Fore, Style

# Initialize global variables
found_counter = 0
current_state = 0
total_url = 0

# Argument parsing setup
parser = argparse.ArgumentParser(description="WhatsMyName for ARCADE-DB")
parser.add_argument("--no-progress", "-np", action="store_true", help="Disable progression")
parser.add_argument("--print-all", "-a", action="store_true", help="Print also not found")
parser.add_argument("--print-error", "-e", action="store_true", help="Print error, status_code and timeout")
parser.add_argument("--used-account-testmode", "-u", action="store_true", help="Use already logged-in accounts to check correct operation")
parser.add_argument("username", nargs="?", default="ArgUmEnt_nOt_spEcIfIEd", help="Target Username")
parser.add_argument("--timeout", "-t", type=int, help="Modify request timeout, default = 2")
parser.add_argument("--minimal", "-m", action="store_true", help="Minimal print")
parser.add_argument("--category", "-c", type=str, help="Filter searches by category")

args = parser.parse_args()

used_account_test_mode = args.used_account_testmode
account = args.username
if account == "ArgUmEnt_nOt_spEcIfIEd" and not used_account_test_mode:
    parser.print_help()
    exit()

print_all_mode = args.print_all
print_error_mode = args.print_error
no_progress = not args.no_progress
minimal_mode = args.minimal

if minimal_mode:
    no_progress = False

timeout_time = args.timeout if args.timeout else 2

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}

def requestsCheck(e_string, m_string, formatted_url, semaphore, e_code, m_code):
    global found_counter
    global current_state
    try:
        response = requests.get(formatted_url, headers=headers, timeout=timeout_time)
        status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")

        if status_code == e_code and e_string in decoded_html:
            found = False if m_string in decoded_html else True
            print_line = Fore.GREEN + f" ➤ {formatted_url}" + Style.RESET_ALL if found else Fore.RED + f" ➤ {formatted_url}" + Style.RESET_ALL
            if found:
                found_counter += 1
            if found or print_all_mode:
                print(print_line)
        elif print_error_mode and status_code != m_code:
            print(Fore.RED + " ➤", Style.RESET_ALL, formatted_url, ":", Back.RED + Fore.WHITE, status_code, Style.RESET_ALL, "e_code =", Back.GREEN, e_code, Style.RESET_ALL)
    except Exception as e:
        if print_error_mode:
            print(Back.RED + Fore.WHITE, f"{e} url={formatted_url}", Style.RESET_ALL)
    finally:
        semaphore.release()
        current_state += 1
        if no_progress:
            advance = f"Progress: {current_state}/{total_url} ({(current_state/total_url)*100:.2f}%)"
            print(advance, end="\r", flush=True)

def main(uri_checks):
    global total_url
    semaphore = threading.Semaphore(30)
    threads = []
    total_url = len(uri_checks)
    for site in uri_checks:
        url = site.get("uri_check")
        e_string = site.get("e_string")
        m_string = site.get("m_string")
        e_code = site.get("e_code")
        m_code = site.get("m_code")
        formatted_url = url.format(account=account)
        thread = threading.Thread(target=requestsCheck, args=(e_string, m_string, formatted_url, semaphore, e_code, m_code))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "wmn-data.json")
with open(file_path, encoding='utf-8') as f:
    data = json.load(f)

uri_checks = data.get("sites", [])
if args.category:
    uri_checks = [site for site in uri_checks if site.get("cat") == args.category]

init()

if __name__ == "__main__":
    start_time = time.time()
    main(uri_checks)
    execution_time = time.time() - start_time

    if not minimal_mode:
        print(Back.BLACK + f"Progress: {current_state}/{total_url} ({(current_state/total_url)*100:.2f}%) {found_counter}/{total_url} found {execution_time:.2f}s" + Style.RESET_ALL)
