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
import os
import signal
import sys
from pathlib import Path

import click
from rich.progress import MofNCompleteColumn, Progress

from database import Database
from gilda_arinc import GildaArinc
from gilda_xml import GildaChannelsXml, GildaXml

__author__ = "Michael Wolf aka Mictronics"
__copyright__ = "2025, (C) Michael Wolf"
__license__ = "GPL v3+"
__version__ = "1.0.0"


@click.group(invoke_without_command=True)
@click.version_option(version=__version__)
def cli():
    """
    GILDA parser

    Use COMMAND --help for help of specific commands.

    License GPL-3+ (C) 2025 Michael Wolf, www.mictronics.de
    """

    # Setup signal handlers for graceful termination
    def signal_handler(signal, frame):
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


@cli.command(
    "convert", help="Read and parse GILDA export XML files into SQLite database."
)
@click.option(
    "-s",
    "--structures",
    help="Insert or update existing data structures. Mandatory with empty database.",
    type=bool,
    is_flag=True,
)
@click.option(
    "-a",
    "--arinc",
    help="Parse additional ARINC Fido definition and insert them into the database.",
    is_flag=False,
    flag_value="ARINC.conf",
)
@click.argument(
    "input_path",
    type=click.Path(dir_okay=True, exists=True, readable=True),
)
@click.argument(
    "output_file",
    type=click.Path(file_okay=True, exists=True, readable=True, writable=True),
)
def convert(structures, arinc, input_path, output_file):
    with Progress(
        *Progress.get_default_columns(), MofNCompleteColumn(), transient=True
    ) as progress:
        total = 0
        # First need the channels before processing channel XML files
        # Found channel IDs will be assigned to existing data structures
        ch_task = progress.add_task("[green]Channels", total=total)
        for root, _dirs, files in os.walk(input_path):
            total += len(files)
            progress.update(ch_task, total=total)
            for file in files:
                progress.update(ch_task, advance=1)
                if file.lower() == "channels.xml":
                    file_path = os.path.join(root, file)
                    with GildaChannelsXml(output_file) as xml:
                        xml.parse(file_path)
        progress.remove_task(ch_task)

        # Process GILDA XML files from input path
        # Walk through the input directory and find XML files
        xml_task = progress.add_task("[red]XML", total=total)
        for root, _dirs, files in os.walk(input_path):
            for file in files:
                progress.update(xml_task, advance=1)
                if file.endswith((".XML", ".xml")):
                    file_path = os.path.join(root, file)
                    with GildaXml(output_file, structures) as xml:
                        xml.parse(file_path)
        progress.remove_task(xml_task)

        if arinc is not None:
            arinc_task = progress.add_task("[blue]ARINC", total=total)
            for root, _dirs, files in os.walk(input_path):
                for file in files:
                    progress.update(arinc_task, advance=1)
                    if file == arinc:
                        file_path = os.path.join(root, file)
                        with GildaArinc(output_file) as arinc:
                            arinc.parse(file_path)
            progress.remove_task(arinc_task)


@cli.command(
    "create",
    help="Create a new database, overwriting existing files.",
)
@click.argument(
    "output_file",
    type=click.Path(file_okay=True, exists=False),
)
def create(output_file):
    # Handle database creation when [--create] was given
    sql_file_path = Path(__file__).parent / "create_gilda_database.sql"
    # Check if SQL file exists
    if not sql_file_path.is_file():
        print(f"SQL file for database creation not found: '{sql_file_path}'")
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
    with Database(output_file) as db:
        db.create(create_sql)


main = cli
if __name__ == "__main__":
    main()
