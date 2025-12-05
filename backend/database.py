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
            self.database = sqlite3.connect(
                database_path, isolation_level="DEFERRED")
            self.cursor = self.database.cursor()
            self.database.execute("PRAGMA journal_mode = TRUNCATE;")
            self.database.execute("PRAGMA foreign_keys = ON;")
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

    def view_data_structures(self):
        """Retrieve all data structures from the database."""
        row = self.cursor.execute("SELECT * FROM ViewDataStructures;")
        return [
            {"id": r[0],
             "name": r[1],
             "source": r[2],
             "channel": r[3]} for r in row.fetchall()
            ]