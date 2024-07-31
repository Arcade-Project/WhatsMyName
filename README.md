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

- [ ] stdout csv
- [ ] tor & proxy support
- [ ] profile extraction from found profiles
- [ ] organize export with categories
- [x] data export to json and csv
- [x] change print_all to print_not_founds and print_false_positives
- [x] solve the problem of false current_state and percentage
- [x] number of threads argument
- [x] Compare GITHUB API SHA key with local file version
- [x] argparse
- [x] search by cat
- [x] use also m_string to verify url
- [x] multiThreading
- [x] requests session

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
usage: main.py [-h] [--timeout TIMEOUT] [--threads THREADS] [--list-cat]
               [--update] [--print-not-founds] [--print-false-positives]
               [--print-error] [--export-csv] [--export-json]
               [username] [category]

WhatsMyName by ARCADE-DB

positional arguments:
  username              Target Username
  category              Filter searches by category

options:
  -h, --help            show this help message and exit
  --timeout TIMEOUT, -t TIMEOUT
                        Modify request timeout, default = 2
  --threads THREADS, -th THREADS
                        Modify max concurrent threads, default = 60
  --list-cat, -lc       List all available categories and exit
  --update, -u          Update wmn-data.json and exit
  --print-not-founds, -n
                        Print not founds
  --print-false-positives, -fp
                        Print false positives
  --print-error, -e     Print error, status code, and timeout
  --export-csv, -csv    Export search in csv
  --export-json, -json  Export search in json
```
