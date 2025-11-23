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
Input path and output database must be specified.
usage: gilda_parser [-h] [--create DATABASE] [-s] [-a ARINC_CONFIGURATION_FILE] [--version] [input] [output]

Read and parse GILDA export XML files into SQLite database.

positional arguments:
  input                 Input path that contains GILDA export XML files.
  output                Output SQLite database file, including path.

options:
  -h, --help            show this help message and exit
  --create DATABASE     Create a new database, overwriting existing files.
  -s, --structures      Insert or update existing data structures. Mandatory with empty database.
  -a ARINC_CONFIGURATION_FILE, --arinc ARINC_CONFIGURATION_FILE
                        Parse additional ARINC Fido definition and insert them into the database.
  --version             show program's version number and exit
```
