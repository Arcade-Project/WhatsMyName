import sys
import json
import time
import requests
import threading
from colorama import init, Back, Fore, Style

if len(sys.argv) > 1:
    account = sys.argv[1]
else:
    print({"error": "invalid argument"})
    sys.exit()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
}


def requestsCheck(
    e_string,
    m_string,
    formatted_url,
    semaphore,
):
    global current_state
    global total_url
    try:
        response = session.get(formatted_url, headers=headers, timeout=2)
    except Exception:
        semaphore.release()
        return
    else:
        status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")
        if status_code < 400:
            if e_string in decoded_html:
                reply = f"Found: {formatted_url}"
                found = True
                if m_string in decoded_html:
                    found = False
                if found:
                    print(Fore.GREEN + reply + Style.RESET_ALL)
                    global found_counter
                    found_counter += 1
    print(
        f"Progress: {current_state}/{total_url} ({(current_state/total_url)*100:.2f}%)     ",
        end="\r",
        flush=True,
    )
    semaphore.release()


def main(uri_checks):
    global current_state
    for site in uri_checks:
        current_state += 1
        url = site.get("uri_check")
        e_string = site.get("e_string")
        m_string = site.get("m_string")

        formatted_url = url.format(account=account)

        semaphore.acquire()
        thread = threading.Thread(
            target=requestsCheck,
            args=(
                e_string,
                m_string,
                formatted_url,
                semaphore,
            ),
        )
        threads.append(thread)
        thread.start()


# def global variable
found_counter = 0
current_state = 0

threads = []
semaphore = threading.Semaphore(30)

with open("wmn-data.json") as f:
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
