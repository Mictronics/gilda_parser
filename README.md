# GILDA Parser

Parser demo that is reading the GILDA export file in XML format into an SQLite database.

This is a project for development guidance and demonstration purpose.

## Installation

Clone repository: `git clone https://github.com/Mictronics/gilda_parser`.

Create Python environment `python3 -m venv ~/gilda_parser/.venv`.

## Dependencies

Install Python requirements with `pip install -r requirements.txt`

The GILDA viewer frontend development requires NodeJS, NPM and Vue CLI to be installed globally.

- NodeJs and NPM see [https://nodejs.org/en/download](https://nodejs.org/en/download)
- Install Vue CLI `npm install -g @vue/cli`

## Run

Activate Python environment `source ~/gilda_parser/.venv/bin/activate`

Create empty database `~/gilda_parser/gilda_parser.py create ./output/database_v1004.sqlite`

Convert Gilda files into database `~/gilda_parser/gilda_parser.py convert -s ./gilda/1004 ./output/database_v1004.sqlite`

Including ARINC from file ARINC.conf `~/gilda_parser/gilda_parser.py convert -s -a ./gilda/1004 ./output/database_v1004.sqlite`

```bash
$ python3 gilda_parser.py -h
  Use COMMAND --help for help of specific commands.

  License GPL-3+ (C) 2025 Michael Wolf, www.mictronics.de

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  convert  Read and parse GILDA export XML files into SQLite database.
  create   Create a new database, overwriting existing files.

$ python gilda_parser.py convert --help
Usage: gilda_parser.py convert [OPTIONS] INPUT_PATH OUTPUT_FILE

  Read and parse GILDA export XML files into SQLite database.

Options:
  -s, --structures  Insert or update existing data structures. Mandatory with
                    empty database.
  -a, --arinc TEXT  Parse additional ARINC Fido definition and insert them
                    into the database.
  --help            Show this message and exit.

$ python gilda_parser.py create --help
Usage: gilda_parser.py create [OPTIONS] OUTPUT_FILE

  Create a new database, overwriting existing files.

Options:
  --help  Show this message and exit.
```
