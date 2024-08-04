from concurrent.futures import ThreadPoolExecutor
from wmn import globals


def exec_concurrent_self_check(uri_checks, session, report_type):
    from wmn import update_current_state
    from .self_check_requests import self_check_requests

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
            known = site.get("known")

            # Submit the self_check_requests function to the executor
            for username in known:
                formatted_url = url.format(account=username)
                futures.append(
                    executor.submit(
                        self_check_requests,
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
                    output += arg
                print(output)
        print(globals.found_counter, "accounts found")
        print("erros counter :", globals.errors_counter)
        if report_type == "detailed":
            report_md = ""
            i = 0
            for report_list in globals.errors_list:
                i = i + 1
                report_md = (
                    report_md
                    + f"""\
## {i}. Name : **{report_list[0]}**

- **Formatted URL :** [{report_list[1]}]({report_list[1]})
- **e_code expected :** `{report_list[3]["e_code"]}`
- **m_code expected :** `{report_list[3]["m_code"]}`

### Results

- **e_code :** `{report_list[2]["e_code"]}`
- **e_string :** `{report_list[2]["e_string"]}`
- **m_code :** `{report_list[2]["m_code"]}`
- **m_string :** `{report_list[2]["m_string"]}`

### Answer details

- **Received HTTP Status Code :** `{report_list[3]["received_status_code"]}`

### Errors detected

{errors_messages(report_list[2]["e_code"], report_list[2]["e_string"], report_list[2]["m_code"], report_list[2]["m_string"])}

---
"""
                )

            with open("self_check.md", "w") as file:
                file.write(report_md)
        elif report_type == "summary":
            with open("self_check.md", "w") as file:
                for line in globals.errors_list:
                    file.write(str(line) + "\n")


def errors_messages(e_code, e_string, m_code, m_string):
    output = ""
    if e_code != e_string:
        output = (
            output
            + "- [ ] Validation of `e_code` and `e_string` cannot be different.\n"
        )
    if m_code != m_string and m_code != e_code:
        output = (
            output
            + "- [ ] Validation of `m_code` and `m_string` cannot be different if `m_code` != `e_string`.\n"
        )
    if e_string and m_string:
        output = output + "- [ ] `e_string` and `m_string` cannot both be valid.\n"
    return output
