# GILDA Parser

Parser demo that is reading the GILDA export file in XML format into an SQLite database.

## Installation

Clone repository: `git clone https://github.com/Mictronics/gilda_parser`.

Create Python environment `python3 -m venv ~/gilda_parser/.venv`.

## Run

Activate Python environment `source ~/gilda_parser/.venv/bin/activate`

Create empty database `~/gilda_parser/gilda_parser.py --create ./output/database_v1004.sqlite`

Convert Gilda files into database `~/gilda_parser/gilda_parser.py ./gilda/1004 ./output/database_v1004.sqlite`

```bash
$ python3 gilda_parser.py -h
positional arguments:
  input              Input path that contains GILDA export XML files.
  output             Output SQLite database file, including path.

options:
  -h, --help         show this help message and exit
  --create DATABASE  Create a new database, overwriting existing files.
  --version          show program's version number and exit

License GPL-3+ (C) 2025 Michael Wolf, www.mictronics.de
```
