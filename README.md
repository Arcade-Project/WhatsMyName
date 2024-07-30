## WMN ARC DB

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
usage: main.py [-h] [--timeout TIMEOUT] [--threads THREADS] [--listcat]
               [--update] [--print-all] [--print-error]
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
  --listcat, -lc        List all available categories
  --update, -u          Update wmn-data.json
  --print-all, -a       Print also not found and false positives
  --print-error, -e     Print error, status code, and timeout
```
