from concurrent.futures import ThreadPoolExecutor
import sys
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
    print(globals.current_state, *args)
    progress_bar()


def exec_concurrent_uri_checks(uri_checks, username, session):
    from wmn import requests_check, update_current_state

    # Use ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=60) as executor:
        futures = []
        for site in uri_checks:
            url = site.get("uri_check")
            e_string = site.get("e_string")
            m_string = site.get("m_string")

            e_code = site.get("e_code")
            m_code = site.get("m_code")

            name = site.get("name")

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
