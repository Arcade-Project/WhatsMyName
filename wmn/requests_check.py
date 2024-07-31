from colorama import Fore, Style
from wmn import globals


def requests_check(e_string, m_string, formatted_url, e_code, m_code, name, session):

    try:
        response = session.get(
            formatted_url, headers=globals.headers, timeout=globals.timeout
        )
    except Exception as e:
        if globals.print_error:
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

        if status_code == e_code:
            if e_string in decoded_html:
                return (Fore.GREEN, "found", Style.RESET_ALL, name, formatted_url)
            elif globals.print_false_positives:
                return (
                    Fore.YELLOW,
                    "false positive",
                    Style.RESET_ALL,
                    name,
                    formatted_url,
                )
        elif globals.print_not_founds or globals.print_error:
            if status_code == m_code:
                if m_string in decoded_html:
                    if globals.print_not_founds:
                        return (
                            Fore.RED,
                            "not found",
                            Style.RESET_ALL,
                            name,
                            formatted_url,
                        )
                else:
                    if globals.print_error:
                        return (
                            Fore.RED,
                            "error no match for e_string and m_string",
                            formatted_url,
                            Style.RESET_ALL,
                        )
            else:
                if globals.print_error:
                    return (
                        Fore.RED,
                        "error no matching status code",
                        formatted_url,
                        Style.RESET_ALL,
                    )
        else:
            return
