from colorama import Fore, Style
from wmn import globals, check_version_status


def colorize_status_color():
    update_status = check_version_status()
    if update_status == "out of date":
        return f"{Fore.RED}{update_status}{Style.RESET_ALL}"
    elif update_status == "up to date":
        return f"{Fore.GREEN}{update_status}{Style.RESET_ALL}"


header = f"""\
=============================
{Fore.YELLOW}WhatsMyName \
{Style.RESET_ALL}by {Fore.MAGENTA}ARCADE DB {Style.RESET_ALL}
wmn-data.json {Fore.RED}is{Style.RESET_ALL} {colorize_status_color()}
"""


def print_header_and_informations():
    infos = f"""\
-----------------------------
total url             : {globals.total_url}
threads               : {globals.max_concurrent_threads}
timeout               : {globals.timeout}
-----------------------------
print not founds      : {globals.print_not_founds}
print false positives : {globals.print_false_positives}
print errors          : {globals.print_errors}
retesting errors      : {globals.retesting_errors}
=============================
"""

    i = header + infos
    print(i)


def print_header():
    h = header + "=============================\n"
    print(h)
