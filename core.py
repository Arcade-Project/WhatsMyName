import os
import json
import time
import argparse
import requests
import threading
from colorama import init, Back, Fore, Style


found_counter = 0
current_state = 0
total_url = 0
json_results = []

# Argument parsing setup
parser = argparse.ArgumentParser(description="WhatsMyName for ARCADE-DB")
parser.add_argument("--catlist", "-cl", action="store_true", help="List all available categories")
parser.add_argument("--no-progress", "-np", action="store_true", help="Disable progression")
parser.add_argument("--print-all", "-a", action="store_true", help="Print also not found")
parser.add_argument("--print-error", "-e", action="store_true", help="Print error, status code, and timeout")
parser.add_argument("--used-account-testmode", "-u", action="store_true", help="Use already logged-in accounts to check correct operation")
parser.add_argument("username", nargs="?", default=None, help="Target Username")
parser.add_argument("--timeout", "-t", type=int, help="Modify request timeout, default = 2")
parser.add_argument("--minimal", "-m", action="store_true", help="Minimal print")
parser.add_argument("--category", "-c", type=str, help="Filter searches by category")
parser.add_argument("--single-site", "-s", type=str, help="Specify a single site by name for the search")
parser.add_argument("--output-json", "-j", action="store_true", help="Output results in JSON format")
args = parser.parse_args()

# Function to print all categories
def print_categories():
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    categories = {site.get("cat") for site in data.get("sites", [])}
    for cat in sorted(categories):
        print(Fore.GREEN + cat + Style.RESET_ALL)


init()
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "wmn-data.json")


if args.catlist:
    print_categories()
    exit()


if not args.username:
    print("Username is required unless --catlist is specified.")
    parser.print_help()
    exit()


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}

def requestsCheck(e_string, m_string, formatted_url, semaphore, e_code, m_code):
    global found_counter, current_state, json_results
    try:
        response = requests.get(formatted_url, headers=headers, timeout=args.timeout or 2)
        status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")
        found = False
        if status_code == e_code and e_string in decoded_html:
            found = not (m_string in decoded_html)
            print_line = Fore.GREEN + f" ➤ {formatted_url}" + Style.RESET_ALL if found else Fore.RED + f" ➤ {formatted_url}" + Style.RESET_ALL
            if found:
                found_counter += 1
            if found or args.print_all:
                print(print_line)
            json_results.append({"url": formatted_url, "status": "found" if found else "not found"})
        elif args.print_error and status_code != m_code:
            print(Fore.RED + " ➤", Style.RESET_ALL, formatted_url, ":", Back.RED + Fore.WHITE, status_code, Style.RESET_ALL, "e_code =", Back.GREEN, e_code, Style.RESET_ALL)
            json_results.append({"url": formatted_url, "status": "error"})
    except Exception as e:
        if args.print_error:
            print(Back.RED + Fore.WHITE, f"{e} url={formatted_url}", Style.RESET_ALL)
        json_results.append({"url": formatted_url, "status": "exception"})
    finally:
        semaphore.release()
        current_state += 1
        if not args.no_progress:
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
        formatted_url = url.format(account=args.username)
        thread = threading.Thread(target=requestsCheck, args=(e_string, m_string, formatted_url, semaphore, e_code, m_code))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if args.output_json:
        print(json.dumps({"results": json_results}, indent=4))

with open(file_path, encoding='utf-8') as f:
    data = json.load(f)

uri_checks = data.get("sites", [])
if args.category:
    uri_checks = [site for site in uri_checks if site.get("cat") == args.category]
if args.single_site:
    uri_checks = [site for site in uri_checks if site.get("name") == args.single_site or site.get("uri_check") == args.single_site]

if __name__ == "__main__":
    start_time = time.time()
    main(uri_checks)
    execution_time = time.time() - start_time
    if not args.minimal:
        print(Back.BLACK + f"Progress: {current_state}/{total_url} ({(current_state/total_url)*100:.2f}%) {found_counter}/{total_url} found {execution_time:.2f}s" + Style.RESET_ALL)
