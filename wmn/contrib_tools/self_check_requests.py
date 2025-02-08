from wmn import globals, update_errors_counter


def self_check_requests(
    e_string, m_string, formatted_url, e_code, m_code, name, cat, session
):

    try:
        response = session.get(
            formatted_url, headers=globals.headers, timeout=globals.timeout
        )
    except Exception as e:
        globals.requests_errors_list.append([name, formatted_url, str(e)])
        return (
            "error",
            formatted_url,
            str(e),
        )
    else:
        received_status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")
        results = {
            "e_code": False,
            "e_string": False,
            "m_code": False,
            "m_string": False,
        }

        if received_status_code == "443":
            globals.status_code_errors_list.append(
                [name, formatted_url, received_status_code]
            )
        if e_code == received_status_code:
            results["e_code"] = True

        if e_string in decoded_html:
            results["e_string"] = True

        if m_code == received_status_code:
            results["m_code"] = True

        if m_string in decoded_html:
            results["m_string"] = True

        if (
            results["e_code"] != results["e_string"]
            or results["m_code"] != results["m_string"]
            and results["m_code"] != results["e_code"]
            or results["e_string"]
            and results["m_string"]
        ):
            update_errors_counter()
            globals.errors_list.append(
                [
                    name,
                    formatted_url,
                    results,
                    {
                        "received_status_code": received_status_code,
                        "e_code": e_code,
                        "m_code": m_code,
                        "e_string": e_string,
                        "m_string": m_string,
                    },
                ]
            )
            return

        # for valid username check
        # if messages["e_code"] and messages["e_string"] and not messages["m_string"]:
        #     print(name, formatted_url, messages)
