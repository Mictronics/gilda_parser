# This file is part of the GILDA viewer.
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
import sqlite3


class Database:
    """Database connection and operations for GILDA viewer backend."""

    def __init__(self, database_path):
        # Connect to database
        try:
            self.database = sqlite3.connect(database_path, isolation_level="DEFERRED")
            self.cursor = self.database.cursor()
            self.database.commit()
        except Exception as e:
            print("Connecting database failed.")
            print(f"Error was: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.database.close()

    def close(self):
        """Close the database connection."""
        self.__exit__(None, None, None)

    def get_data_structures(self):
        """Retrieve all data structures from the database."""
        rows = self.cursor.execute("SELECT * FROM ViewDataStructures;")
        return [
            {"id": r[0], "name": r[1], "source": r[2], "channel": r[3]}
            for r in rows.fetchall()
        ]

    def get_parameter_fields(self, id):
        """Retrieve all parameter fields for a specific ID from database"""
        rows = self.cursor.execute(
            "SELECT * FROM ViewParameterFields where DataStructureId=?;", [id]
        )
        return [
            {
                "id": r[0],
                "name": r[1],
                "reference": r[2],
                "size": r[3],
                "offset": r[4],
                "type": r[5],
                "unit": r[10],
                "desc": r[11],
                "min": r[12],
                "max": r[13],
                "lowBit": r[14],
                "highBit": r[15],
                "comment": r[16],
            }
            for r in rows.fetchall()
        ]

    def get_enumerations(self, id):
        """Retrieve all enumeration values for a specific parameter ID from database"""
        rows = self.cursor.execute(
            "SELECT * FROM ViewParameterEnumValues where ParameterField=?;", [id]
        )
        return [
            {
                "id": r[0],
                "name": r[1],
                "value": r[2],
                "definition": r[3],
                "comment": r[4],
            }
            for r in rows.fetchall()
        ]

    def get_parameter_arinc(self, id):
        rows = self.cursor.execute(
            "SELECT * FROM ViewParameterArinc where ParameterFieldsId=?;", [id]
        )
        return [
            {
                "label": r[0],
                "name": r[1],
                "desc": r[2],
                "fifo": r[3],
                "type": r[4],
                "offset": r[5],
                "size": r[6],
                "unit": r[7],
                "min": r[8],
                "max": r[9],
                "scale": r[10],
            }
            for r in rows.fetchall()
        ]
