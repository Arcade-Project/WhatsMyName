import os
import json
import time
import argparse
import requests
import threading
from colorama import init, Back, Fore, Style

parser = argparse.ArgumentParser(description="WhatsMyName for ARCADE-DB")
# parser.add_argument('--output', '-o', action='store_true', help='')
# parser.add_argument("--json", action="store_true", help="")
parser.add_argument(
    "--no-progress", "-np", action="store_true", help="Disable progression"
)
parser.add_argument(
    "--print-all", "-a", action="store_true", help="Print also not found"
)
parser.add_argument(
    "--print-error", "-e", action="store_true", help="Print error, status_code and timeout"
)
parser.add_argument(
    "--used-account-testmode", "-u", action="store_true", help="Use already logged-in accounts to check correct operation"
)
parser.add_argument(
    "username", nargs="?", default="ArgUmEnt_nOt_spEcIfIEd", help="Target Username"
)
parser.add_argument("--timeout", "-t", type=int, help="Modify request timeout, default = 2")
parser.add_argument("--minimal", "-m", action="store_true", help="Minimal print")

# parser.add_argument(
#     "-s",
#     "--singlesearch",
#     nargs="*",
#     help="Single site search",
# )
# parser.add_argument(
#     "-f",
#     "--fulllist",
#     action="store_true",
#     help="View full sites list on Project WMN | Find site name before doing a single search",
# )
# parser.add_argument(
#     "-c",
#     "--countsites",
#     action="store_true",
#     help="Number of sites currently supported on Project WhatsMyName",
# )

args = parser.parse_args()

used_account_test_mode = args.used_account_testmode
account = args.username
if account == "ArgUmEnt_nOt_spEcIfIEd":
    if not used_account_test_mode:
        parser.print_help()
        exit()

print_all_mode = args.print_all
print_error_mode = args.print_error

no_progress = not args.no_progress

minimal_mode = args.minimal

if minimal_mode:
    no_progress = False

timeout_time = args.timeout
if timeout_time == None:
    timeout_time = 2


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}


def requestsCheck(
    e_string,
    m_string,
    formatted_url,
    semaphore,
    e_code,
    m_code,
):
    global found_counter
    global current_state
    global total_url
    global last_print
    try:
        response = session.get(formatted_url, headers=headers, timeout=timeout_time)
    except Exception as e:
        if print_error_mode:
            if "timed out" or "timeout" in str(e):
                print(Fore.YELLOW + f" ➤ {formatted_url}", Style.RESET_ALL)
            else:
                print(
                    Back.RED + Fore.WHITE, f"{e} url={formatted_url}", Style.RESET_ALL
                )
        semaphore.release()
        current_state += 1
        return
    else:
        status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")

        if status_code == e_code:
            if e_string in decoded_html:
                reply = f" ➤ {formatted_url}"
                found = True
                if m_string in decoded_html:
                    reply = f" ➤ {formatted_url}"
                    found = False
                if found:
                    if no_progress:
                        print("\r" + " " * len(last_print), end="\r", flush=True)
                    if minimal_mode:
                        print(formatted_url)
                    else:
                        print(Fore.GREEN + reply + Style.RESET_ALL, end="\n")
                    found_counter += 1
                elif print_all_mode:
                    if no_progress:
                        print("\r" + " " * len(last_print), end="\r", flush=True)
                    print(Fore.RED + reply + Style.RESET_ALL, end="\n")

        elif print_error_mode:
            if status_code != m_code:
                print(
                    Fore.RED,
                    " ➤",
                    Style.RESET_ALL,
                    formatted_url,
                    ":",
                    Back.RED + Fore.WHITE,
                    status_code,
                    Style.RESET_ALL,
                    "e_code = ",
                    Back.GREEN,
                    e_code,
                    Style.RESET_ALL,
                )

    if no_progress:
        advance = f"Progress: {current_state}/{total_url} ({(current_state/total_url)*100:.2f}%)"
        last_print = advance
        print(
            advance,
            end="\r",
            flush=True,
        )
    semaphore.release()
    current_state += 1


def main(uri_checks):
    global account
    for site in uri_checks:
        url = site.get("uri_check")
        e_string = site.get("e_string")
        m_string = site.get("m_string")
        if used_account_test_mode:
            account = site.get("known")
            account = account[0]

        e_code = site.get("e_code")
        m_code = site.get("m_code")

        formatted_url = url.format(account=account)

        semaphore.acquire()
        thread = threading.Thread(
            target=requestsCheck,
            args=(
                e_string,
                m_string,
                formatted_url,
                semaphore,
                e_code,
                m_code,
            ),
        )
        threads.append(thread)
        thread.start()


# def global variable
last_print = ""
found_counter = 0
current_state = 0

threads = []
semaphore = threading.Semaphore(30)

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "wmn-data.json")

with open(file_path) as f:
    data = json.load(f)

uri_checks = data.get("sites", [])
total_url = len(uri_checks)

init()  # Init for colorama

# start
start_time = time.time()

if __name__ == "__main__":
    with requests.Session() as session:
        main(uri_checks)

for thread in threads:
    thread.join()

end_time = time.time()
execution_time = end_time - start_time

print(
    "",
    end="\r",
    flush=True,
)

print(
    Back.BLACK
    + f"Progress: {current_state}/{total_url} ({(current_state/total_url)*100:.2f}%) {found_counter}/{total_url} found {execution_time:.2f}s"
    + Style.RESET_ALL,
    end="\n",
)
