from colorama import Fore, Style

from . import globals
from .helper import update_current_state


def requests_check(e_string, m_string, formatted_url, e_code, m_code, name, session):
    try:
        response = session.get(
            formatted_url, headers=globals.headers, timeout=globals.timeout
        )
    except Exception as e:
        if globals.print_error_mode:
            print(
                globals.current_state,
                Fore.RED,
                "🐛",
                "error",
                formatted_url,
                e,
                Style.RESET_ALL,
            )
        update_current_state()
        return
    else:
        status_code = response.status_code
        decoded_html = response.content.decode("utf-8", errors="ignore")

        if status_code == e_code:
            if e_string in decoded_html:
                print(
                    globals.current_state,
                    Fore.GREEN,
                    "found",
                    Style.RESET_ALL,
                    name,
                    formatted_url,
                )
            elif globals.print_all_mode:
                print(
                    globals.current_state,
                    Fore.YELLOW,
                    "false positive",
                    Style.RESET_ALL,
                    formatted_url,
                )
        elif globals.print_all_mode:
            if status_code == m_code:
                if m_string in decoded_html:
                    print(
                        globals.current_state,
                        Fore.RED,
                        "not found",
                        Style.RESET_ALL,
                        name,
                        formatted_url,
                    )
                """
                There is no 'else' here because I don't think the information is useful.
                If the 'else' were executed, it would be because the JSON contains an incorrect value.
                """
    update_current_state()
