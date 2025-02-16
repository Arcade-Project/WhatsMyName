from wmn import globals
from colorama import Fore, Style


def requests_check(
    e_string, m_string, formatted_url, e_code, m_code, name, session
):
    from wmn import update_found_counter

    try:
        response = session.get(
            formatted_url, headers=globals.headers, timeout=globals.timeout
        )
    except Exception as e:

        if globals.retesting_errors:
            globals.requests_errors_list.append(
                [formatted_url, str(e).replace(",", ";")])

        if (
            globals.export_csv or
            globals.export_json
        ):
            globals.csv_list.append(f'error, "{formatted_url}", "{
                                    str(e).replace(",", ";")}"')
        if globals.print_errors:
            return (
                Fore.RED,
                "error",
                formatted_url,
                str(e),
                Style.RESET_ALL,
            )
        return
    else:
        received_status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")

        # positive hit
        if (
            e_code == received_status_code
            and e_string in decoded_html
            and m_string not in decoded_html
        ):

            if globals.export_csv or globals.export_json:
                globals.csv_list.append(f'found, "{name}", "{formatted_url}"')
            update_found_counter()
            return (Fore.GREEN, "found", Style.RESET_ALL, name, formatted_url)
        # negative hit
        elif globals.print_not_founds:
            if m_code == received_status_code and m_string in decoded_html:
                if globals.export_csv or globals.export_json:
                    globals.csv_list.append(
                        f'not found, "{name}", "{formatted_url}"')
                return (
                    Fore.RED,
                    "not found",
                    Style.RESET_ALL,
                    name,
                    formatted_url,
                )
            else:
                return (
                    Fore.RED,
                    "error",
                    formatted_url,
                    "wrong definition in wmn-data.json",
                    Style.RESET_ALL,
                )
