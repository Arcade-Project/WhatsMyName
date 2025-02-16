from wmn import globals
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def exec_concurrent_uri_checks(uri_checks, username, session):
    from wmn import (
        requests_check,
        update_current_state,
        retesting_errors,
        export_csv,
        export_json,
        print_and_update_progress
    )

    # Use ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(
        max_workers=globals.max_concurrent_threads
    ) as executor:
        futures = []
        for site in uri_checks:
            url = site.get("uri_check")
            e_string = site.get("e_string")
            m_string = site.get("m_string")

            e_code = site.get("e_code")
            m_code = site.get("m_code")

            name = site.get("name")

            # cat = site.get("cat")
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
                    session,
                )
            )
        for future in futures:
            update_current_state()
            output = ""
            if future.result():
                for arg in future.result():
                    output += arg.strip() + " "
                print_and_update_progress(output)
        print(globals.found_counter, "accounts found")

        if globals.retesting_errors:
            retesting_errors()

        if globals.export_csv or globals.export_json:
            now = datetime.now()
            timestamp = now.strftime("%H-%M-%S")

            if globals.export_csv:
                export_csv(timestamp)

            if globals.export_json:
                export_json(timestamp)
