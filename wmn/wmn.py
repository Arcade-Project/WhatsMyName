import os
import sys
import json
import argparse
import requests
from colorama import init, Fore, Style

from wmn import (
    print_categories,
    exec_concurrent_uri_checks,
    check_and_update_file,
    print_header_and_informations,
    print_header,
    set_total_url,
    set_timeout,
    set_max_concurrent_threads,
    set_username,
    enable_print_not_founds,
    enable_print_false_positives,
    enable_print_errors,
    enable_export_csv,
    enable_export_json,
    enable_self_check,
)

from .contrib_tools import concurrent_self_check

# colorama init
init()

parser = argparse.ArgumentParser(description="WhatsMyName by ARCADE-DB")
parser.add_argument("username", nargs="?", help="Target Username")
parser.add_argument(
    "--categories",
    "-cat",
    type=str,
    help="Filter searches by category",
)
parser.add_argument(
    "--timeout",
    "-t",
    type=int,
    help="Modify time to wait for response to requests, default = 30",
)
parser.add_argument(
    "--threads", "-th", type=int, help="Modify max concurrent threads, default = 100"
)
parser.add_argument(
    "--list-cat",
    "-lc",
    action="store_true",
    help="List all available categories and exit",
)
parser.add_argument(
    "--update", "-u", action="store_true", help="Update wmn-data.json and exit"
)
parser.add_argument(
    "--print-not-founds",
    "-n",
    action="store_true",
    help="Print sites where the username was not found",
)
parser.add_argument(
    "--print-false-positives", "-fp", action="store_true", help="Print false positives"
)
parser.add_argument(
    "--print-errors",
    "-e",
    action="store_true",
    help="Print errors messages: connection, status code, and timeout",
)
parser.add_argument(
    "--self-check",
    choices=["summary", "detailed"],
    help="Generate an error report: summary or detailed",
)
parser.add_argument("--export", "-E", type=str, help="Export search in csv or json")
# parser.add_argument(
#     "--no-color", action="store_true", help="Don't color terminal output"
# )
# parser.add_argument("--no-progressbar", action="store_true", help="Hide progressbar")
# parser.add_argument("--site", "-s", type=str, help="Search only on specified sites")


args = parser.parse_args()

username = args.username

if args.export:
    set_username(username)
    if args.export == "csv":
        enable_export_csv()
    elif args.export == "json":
        enable_export_json()
    else:
        print(
            Fore.RED,
            "error, invalid export format",
            Style.RESET_ALL,
        )
        exit()

if args.update:
    check_and_update_file()
    exit()

if args.print_not_founds:
    enable_print_not_founds()

if args.print_false_positives:
    enable_print_false_positives()

if args.print_errors:
    enable_print_errors()

if args.timeout:
    set_timeout(args.timeout)

if args.threads:
    set_max_concurrent_threads(args.threads)

if args.self_check:
    enable_print_not_founds()
    enable_print_false_positives()
    enable_print_errors()
    enable_self_check()

if args.list_cat:
    print_header()
    print_categories()
    exit()


def main():

    current_directory = os.path.abspath(os.path.dirname(__file__))
    parent_directory = os.path.dirname(current_directory)
    file_path = os.path.join(parent_directory, "data", "wmn-data.json")

    if not os.path.exists(file_path):
        print(Fore.RED, "error wmn-data.json not found", Style.RESET_ALL)
        exit()

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    uri_checks = data.get("sites", [])
    if args.categories:
        valid_categories = data.get("categories", [])
        if args.categories not in valid_categories:
            print(
                Fore.RED,
                "error, invalid category name",
                Style.RESET_ALL,
            )
            sys.exit()
        else:
            uri_checks = [
                site for site in uri_checks if site.get("cat") == args.categories
            ]
    set_total_url(len(uri_checks))

    print_header_and_informations()

    with requests.Session() as session:
        if args.self_check:
            report_type = "summary"
            if args.self_check == "detailed":
                report_type = args.self_check

            concurrent_self_check.exec_concurrent_self_check(
                uri_checks, session, report_type
            )
            exit()
        exec_concurrent_uri_checks(uri_checks, username, session)
