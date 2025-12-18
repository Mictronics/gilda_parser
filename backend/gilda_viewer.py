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
import json
import os
import signal
import sys
from pathlib import Path

import click
from flask import Flask, jsonify, render_template, request
from flask_restful import Api, Resource

from database import Database

__author__ = "Michael Wolf aka Mictronics"
__copyright__ = "2025, (C) Michael Wolf"
__license__ = "GPL v3+"
__version__ = "1.0.0"


class GetDatabases(Resource):
    """Return available database files to frontend"""

    def __init__(self, db_files):
        self.db_files = db_files

    def get(self):
        databases = [
            {"name": name, "path": path} for name, path in self.db_files.items()
        ]
        return jsonify(databases)

    def put(self):
        if request.json is None or Path(request.json["database"]).is_file() is False:
            return "Database file not found.", 404
        try:
            with Database(request.json["database"]) as db:
                data = db.get_all_data_structures()
            return jsonify(data)

        except Exception as e:
            return f"{e}", 500


class GetParameterFields(Resource):
    """Load and return parameter fields from database to frontend"""

    def put(self):
        if request.json is None or Path(request.json["database"]).is_file() is False:
            return "Database file not found.", 404

        try:
            id = request.json["id"]
            if not int.is_integer(id):
                id = int(id, base=10)
            with Database(request.json["database"]) as db:
                data = db.get_parameter_fields(id)
            return jsonify(data)

        except Exception as e:
            return f"{e}", 500


class GetEnumerations(Resource):
    """Load and return enumeration values from database to frontend"""

    def put(self):
        if request.json is None or Path(request.json["database"]).is_file() is False:
            return "Database file not found.", 404

        try:
            id = request.json["id"]
            if not int.is_integer(id):
                id = int(id, base=10)
            with Database(request.json["database"]) as db:
                data = db.get_enumerations(id)
            return jsonify(data)

        except Exception as e:
            return f"{e}", 500


class GetParameterArinc(Resource):
    """Load and return ARINC parameters from database to frontend"""

    def put(self):
        if request.json is None or Path(request.json["database"]).is_file() is False:
            return "Database file not found.", 404

        try:
            id = request.json["id"]
            if not int.is_integer(id):
                id = int(id, base=10)
            with Database(request.json["database"]) as db:
                data = db.get_parameter_arinc(id)
            return jsonify(data)

        except Exception as e:
            return f"{e}", 500


class GetDataStructure(Resource):
    """Load and return a data structure from database to frontend"""

    def put(self):
        if request.json is None or Path(request.json["database"]).is_file() is False:
            return "Database file not found.", 404

        try:
            name = request.json["name"]
            with Database(request.json["database"]) as db:
                data = db.get_data_structure(name=name)
            return jsonify(data)

        except Exception as e:
            return f"{e}", 500


@click.group(invoke_without_command=True)
@click.pass_context
@click.argument(
    "input_path",
    type=click.Path(dir_okay=True, exists=True, readable=True),
)
@click.version_option(version=__version__)
def cli(ctx, input_path):
    """
    Read GILDA configuration from SQLite database.

    INPUT_PATH contains GILDA SQlite database files.

    License GPL-3+ (C) 2025 Michael Wolf, www.mictronics.de
    """

    # Setup signal handlers for graceful termination
    def signal_handler(signal, frame):
        sys.exit(0)

    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    db_files = {}

    for root, _dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith((".sqlite", "sqlite3", ".db")):
                file_path = os.path.join(root, file)
                db_files[Path(file_path).stem] = file_path

    app = Flask(__name__, template_folder="../frontend/dist")
    api = Api(app, prefix="/api/v1")
    api.add_resource(GetDatabases, "/databases", resource_class_args=[db_files])
    api.add_resource(GetParameterFields, "/parameters")
    api.add_resource(GetEnumerations, "/enumerations")
    api.add_resource(GetParameterArinc, "/arinc")
    api.add_resource(GetDataStructure, "/structure")

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    app.config.from_file("gilda_viewer_config.json", load=json.load)
    app.run()


main = cli
if __name__ == "__main__":
    main()
