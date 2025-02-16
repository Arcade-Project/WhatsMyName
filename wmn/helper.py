from wmn import globals


def update_current_state():
    globals.current_state = globals.current_state + 1


def update_found_counter():
    globals.found_counter = globals.found_counter + 1


def update_errors_counter():
    globals.errors_counter = globals.errors_counter + 1


def set_total_url(arg):
    globals.total_url = arg


def set_timeout(arg):
    globals.timeout = arg


def set_max_concurrent_threads(arg):
    globals.max_concurrent_threads = arg


def set_username(user):
    globals.username = user


def enable_print_false_positives():
    globals.print_false_positives = True


def enable_print_not_founds():
    globals.print_not_founds = True


def enable_print_errors():
    globals.print_errors = True


def enable_export_csv():
    globals.export_csv = True


def enable_export_json():
    globals.export_json = True


def enable_self_check():
    globals.self_check = True


def enable_retesting_errors():
    globals.retesting_errors = True
