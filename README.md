# ⚡What is WhatsMyName ?

> [!NOTE]
> It is a project that Micah "WebBreacher" Hoffman created in 2015 with the goal of discovering if usernames were used on a given website. He was frustrated with the false positives that were present in the username checkers of that time and so he made his own. Fast forward to today and many people have helped this open-source project evolve into what it is today.
> In May 2023, they decided to remove all verification scripts from the project and concentrate on the heart of the project, its data file (wmn-data.json).

> [!IMPORTANT]
> So in this ARCADE DB repository you'll find the tools you need to use the `wmn-data.json` file to its full potential.

## Directory Architecture

```
WhatsMyName/
├── data
│   └── wmn-data.json
└── wmn
    ├── __init__.py
    ├── concurrent_uri_checks.py
    ├── globals.py
    ├── helper.py
    ├── list_categories.py
    ├── print_infos.py
    ├── requests_check.py
    ├── update.py
    └── wmn.py
├── main.py
├── README.md
├── requirements.txt
```

## TODO

move :
[TODO.md](/TODO.md)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py john
```

```bash
> python main.py -h
usage: main.py [-h] [--categories CATEGORIES] [--timeout TIMEOUT] [--threads THREADS]
               [--list-cat] [--update] [--print-not-founds] [--print-false-positives]
               [--print-errors] [--self-check {summary,detailed}] [--export {json,csv,both}]
               [username]

WhatsMyName by ARCADE-DB

positional arguments:
  username              Target Username

options:
  -h, --help            show this help message and exit
  --categories CATEGORIES, -cat CATEGORIES
                        Filter searches by category
  --timeout TIMEOUT, -t TIMEOUT
                        Modify time to wait for response to requests, default = 30
  --threads THREADS, -th THREADS
                        Modify max concurrent threads, default = 100
  --list-cat, -lc       List all available categories and exit
  --update, -u          Update wmn-data.json and exit
  --print-not-founds, -n
                        Print sites where the username was not found
  --print-false-positives, -fp
                        Print false positives
  --print-errors, -e    Print errors messages: connection, status code, and timeout
  --self-check {summary,detailed}
                        Generate an error report: summary or detailed
  --export {json,csv,both}, -E {json,csv,both}
                        Export search in csv, json, or both
```
