from colorama import Fore, Style
import textwrap
from .update import check_version_status
from wmn import globals


def colorize_status_color():
    update_status = check_version_status()
    if update_status == "out of date":
        return f"{Fore.RED}{update_status}{Style.RESET_ALL}"
    elif update_status == "up to date":
        return f"{Fore.GREEN}{update_status}{Style.RESET_ALL}"


def print_info():
    header = f"""\
===========================
{Fore.YELLOW}WhatsMyName {Style.RESET_ALL}by {Fore.MAGENTA}ARCADE DB {Style.RESET_ALL}
wmn-data.json {Fore.RED}is{Style.RESET_ALL} {colorize_status_color()}
===========================
threads     : {globals.max_concurrent_threads}
timeout     : {globals.timeout}
print all   : {globals.print_all_mode}
print error : {globals.print_error_mode}
===========================
    """
    print(header)


# WhatsMyName by ARCADE DB
# wmn-data.json is up to date
# threads        : 60
# timeout        : 2
# total url      : 625
# print error    : False
# print all      : False
