import sys
from wmn import globals
from colorama import Fore, Style


first_iteration = True


def erase_last_line():
    global first_iteration
    if not first_iteration:
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")
    first_iteration = False


def progress_bar():
    try:

        percent = globals.current_state / globals.total_url * 100
        print(f"Progress: \
        {globals.current_state}/{globals.total_url} ({percent:.2f}%)")
    except Exception as e:
        print(Fore.RED, f"error {e}", Style.RESET_ALL)
        exit(1)


def print_and_update_progress(*args):
    erase_last_line()
    current_state_str = str(globals.current_state)
    current_state_str = current_state_str.rjust(3)
    print(current_state_str, *args)
    progress_bar()
