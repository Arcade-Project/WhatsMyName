from colorama import Fore, Style
from wmn import globals


def requests_check(
    e_string, m_string, formatted_url, e_code, m_code, name, cat, session
):
    from wmn import update_found_counter

    try:
        response = session.get(
            formatted_url, headers=globals.headers, timeout=globals.timeout
        )
    except Exception as e:
        if globals.print_errors or globals.export_json:
            if globals.export_csv or globals.export_json:
                globals.csv_list.append(f'error, "{formatted_url}", "{str(e)}"')
            return (
                Fore.RED,
                "error",
                formatted_url,
                str(e),
                Style.RESET_ALL,
            )
        return
    else:
        status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")
        messages = {
            "e_code": False,
            "e_string": False,
            "m_code": False,
            "m_string": False,
        }

        if e_code == status_code:
            messages["e_code"] = True

        if e_string in decoded_html:
            messages["e_string"] = True

        if m_code == status_code:
            messages["m_code"] = True

        if m_string in decoded_html:
            messages["m_string"] = True

        # if (
        #     messages["e_code"] != messages["e_string"]
        #     or messages["m_code"] != messages["m_string"]
        #     or messages["e_string"]
        #     and messages["m_string"]
        # ):
        #     update_errors_counter()
        #     globals.errors_list.append(
        #         [
        #             name,
        #             formatted_url,
        #             messages,
        #             {
        #                 "status_code": status_code,
        #                 "e_code": e_code,
        #                 "m_code": m_code,
        #                 "e_string": e_string,
        #                 "m_string": m_string,
        #             },
        #         ]
        #     )
        #     return
        # for valid username check
        if messages["e_code"] and messages["e_string"] and not messages["m_string"]:
            update_found_counter()
            return (Fore.GREEN, "found", Style.RESET_ALL, name, formatted_url)
        elif globals.print_not_founds:
            if messages["m_code"] and messages["m_string"] and not messages["e_string"]:
                return (
                    Fore.RED,
                    "not found",
                    Style.RESET_ALL,
                    name,
                    formatted_url,
                )
