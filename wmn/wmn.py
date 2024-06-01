import os
import sys
import json
import argparse
import requests
from colorama import init, Fore, Style

from wmn import (
    print_categories,
    exec_concurrent_uri_checks,
    set_total_url,
    set_timeout,
    enable_print_all_mode,
    enable_print_error_mode,
)

preliminary_parser = argparse.ArgumentParser(
    description="WhatsMyName by ARCADE-DB", add_help=False
)
preliminary_parser.add_argument(
    "--listcat", "-lc", action="store_true", help="List all available categories"
)
preliminary_args, remaining_args = preliminary_parser.parse_known_args()

if preliminary_args.listcat:
    # If --listcat is present, print the categories and exit
    print_categories()
    exit()


parser = argparse.ArgumentParser(description="WhatsMyName by ARCADE-DB")
parser.add_argument("username", help="Target Username")
parser.add_argument(
    "category", nargs="?", default="false", help="Filter searches by category"
)
parser.add_argument(
    "--timeout", "-t", type=int, help="Modify request timeout, default = 2"
)
parser.add_argument(
    "--print-all",
    "-a",
    action="store_true",
    help="Print also not found and false positives",
)
parser.add_argument(
    "--print-error",
    "-e",
    action="store_true",
    help="Print error, status code, and timeout",
)

args = parser.parse_args()

username = args.username

if args.print_all:
    enable_print_all_mode()

if args.print_error:
    enable_print_error_mode()

if args.timeout:
    set_timeout(args.timeout)


def main():

    # colorama init
    init()

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

    with requests.Session() as session:
        exec_concurrent_uri_checks(uri_checks, username, session)
