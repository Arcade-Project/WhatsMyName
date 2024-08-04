from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import sys
import json
from wmn import globals


first_iteration = True


def erase_last_line():
    global first_iteration
    if not first_iteration:
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")
    first_iteration = False


def progress_bar():
    percent = globals.current_state / globals.total_url * 100
    print(f"Progress: {globals.current_state}/{globals.total_url} ({percent:.2f}%)")


def _print(*args):
    erase_last_line()
    current_state_str = str(globals.current_state)
    current_state_str = current_state_str.rjust(3)
    print(current_state_str, *args)
    progress_bar()


def exec_concurrent_uri_checks(uri_checks, username, session):
    from wmn import requests_check, update_current_state

    # Use ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=globals.max_concurrent_threads) as executor:
        futures = []
        for site in uri_checks:
            url = site.get("uri_check")
            e_string = site.get("e_string")
            m_string = site.get("m_string")

            e_code = site.get("e_code")
            m_code = site.get("m_code")

            name = site.get("name")

            cat = site.get("cat")
            # know = site.get("know")

            formatted_url = url.format(account=username)

            # Submit the requests_check function to the executor
            futures.append(
                executor.submit(
                    requests_check,
                    e_string,
                    m_string,
                    formatted_url,
                    e_code,
                    m_code,
                    name,
                    cat,
                    session,
                )
            )
        for future in futures:
            update_current_state()
            output = ""
            if future.result():
                for arg in future.result():
                    output += arg.strip() + " "
                _print(output)
        print(globals.found_counter, "accounts found")
        if globals.export_csv or globals.export_json:
            now = datetime.now()
            timestamp = now.strftime("%H-%M-%S")
            if globals.export_csv:
                file_name = f"wmn-{globals.username}-{timestamp}.csv"
                with open(file_name, "w") as file:
                    for line in globals.csv_list:
                        file.write(line + "\n")
            elif globals.export_json:
                json_output = {
                    "found": {},
                    "not found": {},
                    "false positive": {},
                    "error": {},
                }
                for line in globals.csv_list:
                    raw_line = [part.strip().strip('"') for part in line.split(",")]
                    if len(raw_line) >= 3:
                        category = raw_line[0]
                        name = raw_line[1]
                        url = raw_line[2]

                        if category in json_output:
                            json_output[category][name] = url
                file_name = f"wmn-{globals.username}-{timestamp}.json"
                with open(file_name, "w") as file:
                    file.write(json.dumps(json_output, ensure_ascii=True, indent=2))
