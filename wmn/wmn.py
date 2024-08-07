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
    enable_print_error,
    enable_export_csv,
    enable_export_json,
)

# colorama init
init()

parser = argparse.ArgumentParser(description="WhatsMyName by ARCADE-DB")
parser.add_argument("username", nargs="?", help="Target Username")
parser.add_argument(
    "category", nargs="?", default="false", help="Filter searches by category"
)
parser.add_argument(
    "--timeout", "-t", type=int, help="Modify request timeout, default = 2"
)
parser.add_argument(
    "--threads", "-th", type=int, help="Modify max concurrent threads, default = 60"
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
    "--print-not-founds", "-n", action="store_true", help="Print not founds"
)
parser.add_argument(
    "--print-false-positives", "-fp", action="store_true", help="Print false positives"
)
parser.add_argument(
    "--print-error",
    "-e",
    action="store_true",
    help="Print error, status code, and timeout",
)
parser.add_argument(
    "--export-csv", "-csv", action="store_true", help="Export search in csv"
)
parser.add_argument(
    "--export-json", "-json", action="store_true", help="Export search in json"
)

args = parser.parse_args()

username = args.username

if args.export_csv:
    set_username(username)
    enable_export_csv()

if args.export_json:
    set_username(username)
    enable_export_json()

if args.update:
    check_and_update_file()
    exit()

if args.print_not_founds:
    enable_print_not_founds()

if args.print_false_positives:
    enable_print_false_positives()

if args.print_error:
    enable_print_error()

if args.timeout:
    set_timeout(args.timeout)

if args.threads:
    set_max_concurrent_threads(args.threads)

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
    if args.category != "false":
        valid_categories = data.get("categories", [])
        if args.category not in valid_categories:
            print(
                Fore.RED,
                "ERROR, invalid category name",
                Style.RESET_ALL,
            )
            sys.exit()
        else:
            uri_checks = [
                site for site in uri_checks if site.get("cat") == args.category
            ]
    set_total_url(len(uri_checks))

    print_header_and_informations()

    with requests.Session() as session:
        exec_concurrent_uri_checks(uri_checks, username, session)
