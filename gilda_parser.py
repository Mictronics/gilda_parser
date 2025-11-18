#!python3

# This file is part of the GILDA parser.
#
# Copyright (c) 2025 Michael Wolf <michael@mictronics.de>
#
# GILDA parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# GILDA parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GILDA parser. If not, see http://www.gnu.org/licenses/.
#
import argparse
import os
import signal
import sys
from pathlib import Path
from rich.progress import Progress, MofNCompleteColumn
from database import Database
from gilda_xml import GildaChannelsXml, GildaXml
from gilda_arinc import GildaArinc

__author__ = "Michael Wolf aka Mictronics"
__copyright__ = "2025, (C) Michael Wolf"
__license__ = "GPL v3+"
__version__ = "1.0.0"


def initArgParser(parser=None):
    """Initialize the command line argument parsing."""
    if parser is None:
        return None

    try:
        # Positional arguments
        parser.add_argument(
            "input",
            help="Input path that contains GILDA export XML files.",
            default=None,
            nargs="?",
            type=str,
        )

        parser.add_argument(
            "output",
            help="Output SQLite database file, including path.",
            default=None,
            nargs="?",
            type=str,
        )
        # Optional arguments
        parser.add_argument(
            "--create",
            metavar="DATABASE",
            help="Create a new database, overwriting existing files.",
            default=None,
            type=str,
        )

        parser.add_argument(
            "-s",
            "--structures",
            help="Insert or update existing data structures. Mandatory with empty database.",
            action="store_true",
            default=False,
        )

        parser.add_argument(
            "-a",
            "--arinc",
            metavar="ARINC_CONFIGURATION_FILE",
            help="Parse additional ARINC Fido definition and insert them into the database.",
            dest="arinc_conf",
        )

        parser.set_defaults(deprecated=None)
        parser.add_argument("--version", action="version",
                            version=f"{__version__}")
        args = parser.parse_args()

    except Exception as e:
        print(f"Error initializing argument parser: {e}")
        return None

    return args


def main():
    """Main program function"""
    # Setup signal handlers for graceful termination
    def signal_handler(signal, frame):
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser(
        prog="gilda_parser",
        description="Read and parse GILDA export XML files into SQLite database.",
        epilog="License GPL-3+ (C) 2025 Michael Wolf, www.mictronics.de",
    )
    args = initArgParser(parser)
    if args is None:
        sys.exit(1)  # Exit with error when argument parsing fails

    # Handle database creation when [--create] was given
    if args.create is not None:
        sql_file_path = Path(__file__).parent / "create_gilda_database.sql"
        # Check if SQL file exists
        if not sql_file_path.is_file():
            print(
                f"SQL file for database creation not found: '{sql_file_path}'")
            sys.exit(1)
        # Read SQL file content
        create_sql = None
        try:
            with sql_file_path.open("r", encoding="utf-8") as f:
                create_sql = f.read()
        except Exception as e:
            print(f"Failed to read SQL file '{sql_file_path}': {e}")
            sys.exit(1)
        # Create the database
        with Database(args.create) as db:
            db.create(create_sql)
        sys.exit(0)  # Exit after creating the database

    if args.input is None or args.output is None:
        print("Input path and output database must be specified.")
        parser.print_help()
        sys.exit(1)

    with Progress(*Progress.get_default_columns(), MofNCompleteColumn(), transient=True) as progress:
        total = 0
        # First need the channels before processing channel XML files
        # Found channel IDs will be assigned to existing data structures
        ch_task = progress.add_task("[green]Channels", total=total)
        for root, _dirs, files in os.walk(args.input):
            total += len(files)
            progress.update(ch_task, total=total)
            for file in files:
                progress.update(ch_task, advance=1)
                if file.lower() == "channels.xml":
                    file_path = os.path.join(root, file)
                    with GildaChannelsXml(args.output) as xml:
                        xml.parse(file_path)
        progress.remove_task(ch_task)

        # Process GILDA XML files from input path
        # Walk through the input directory and find XML files
        xml_task = progress.add_task("[red]XML", total=total)
        for root, _dirs, files in os.walk(args.input):
            for file in files:
                progress.update(xml_task, advance=1)
                if file.endswith((".XML", ".xml")):
                    file_path = os.path.join(root, file)
                    with GildaXml(args.output, args.structures) as xml:
                        xml.parse(file_path)
        progress.remove_task(xml_task)

        if args.arinc_conf is not None:
            arinc_task = progress.add_task("[blue]ARINC", total=total)
            for root, _dirs, files in os.walk(args.input):
                for file in files:
                    progress.update(arinc_task, advance=1)
                    if file == args.arinc_conf:
                        file_path = os.path.join(root, file)
                        with GildaArinc(args.output) as arinc:
                            arinc.parse(file_path)
            progress.remove_task(arinc_task)

    sys.exit(0)  # Exit the program


if __name__ == "__main__":
    main()
