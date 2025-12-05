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
#
#
# https://github.com/Nur84/datatables
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-using-flask-restful
# https://www.geeksforgeeks.org/python/python-build-a-rest-api-using-flask/
# https://wpdatatables.com/datatables-alternative/
#
from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api
import argparse
import json
import os
import signal
import sys
from database import Database
from pathlib import Path

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
            help="Input path that contains GILDA SQlite database files.",
            default=None,
            nargs="?",
            type=str,
        )

        parser.set_defaults(deprecated=None)
        parser.add_argument("--version", action="version",
                            version=f"{__version__}")
        args = parser.parse_args()

    except Exception as e:
        print(f"Error initializing argument parser: {e}")
        return None

    return args


class GetDatabases(Resource):
    """Return available database files to frontend"""
    def __init__(self, db_files):
        self.db_files = db_files

    def get(self):
        databases = [{"name": name, "path": path} for name, path in self.db_files.items()]
        return jsonify(databases)


class LoadDatabase(Resource):
    """Load and return selected database to frontend"""
    def put(self):
        if Path(request.json['database']).is_file() is False:
            return "Database file not found.", 404
        try: 
            with Database(request.json['database']) as db:
                data = db.view_data_structures()
            return jsonify(data)
        
        except Exception as e:
            return f"{e}", 500


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
        prog="gilda_viewer",
        description="Read GILDA configuration from SQLite database.",
        epilog="License GPL-3+ (C) 2025 Michael Wolf, www.mictronics.de",
    )
    args = initArgParser(parser)
    if args is None or args.input is None:
        print("Input path with database location must be specified.")
        parser.print_help()
        sys.exit(1)  # Exit with error when argument parsing fails

    db_files = {}

    for root, _dirs, files in os.walk(args.input):
        for file in files:
            if file.endswith((".sqlite", "sqlite3", ".db")):
                file_path = os.path.join(root, file)
                db_files[Path(file_path).stem] = file_path

    app = Flask(__name__,template_folder='../frontend/dist')
    api = Api(app, prefix="/api/v1")
    api.add_resource(GetDatabases, '/databases', resource_class_args=[db_files])
    api.add_resource(LoadDatabase, '/load')

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    app.config.from_file("gilda_viewer_config.json", load=json.load)
    app.run()


if __name__ == "__main__":
    main()
