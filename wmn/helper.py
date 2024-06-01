from wmn import globals


def update_current_state():
    globals.current_state = globals.current_state + 1


def set_total_url(arg):
    globals.total_url = arg


def set_timeout(arg):
    globals.timeout = arg


# ARGS


def enable_print_all_mode():
    globals.print_all_mode = True


def enable_print_error_mode():
    globals.print_error_mode = True
