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
import sqlite3

class Database:
    """Database connection and operations for GILDA parser."""
    def __init__(self, database_path):
        # Connect to database
        try:
            self.database = sqlite3.connect(
                database_path, isolation_level='DEFERRED')
        except Exception as e:
            print("Connecting database failed.")
            print(f"Error was: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.close()

    def close(self):
        """Close the database connection."""
        self.database.close()

    def create(self, sql):
        """Create database schema."""
        cursor = self.database.cursor()
        cursor.execute(sql)
        self.database.commit()

    def get_partitions(self):
        """Retrieve static partition list from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM PartitionList;")
        # Return a dictionary mapping partition names to their IDs
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_structure(self, eng_name: str, src_partition: str):
        """Insert a data structure into the database."""
        cursor = self.database.cursor()
        data = [{"name": eng_name, "src": src_partition},]
        cursor.executemany(
            "INSERT OR IGNORE INTO DataStructures (EngName, SourcePartition) VALUES (:name, :src);",data
        )
        self.database.commit()
        # Retrieve the ID of the inserted structure
        row = cursor.execute("SELECT Id FROM DataStructures WHERE EngName = ?;", [eng_name])
        return row.fetchone()[0]

    def insert_type(self, type):
        """Insert parameter types into the database."""
        cursor = self.database.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO ParameterTypes (Type) VALUES (:type);",[type]
        )
        self.database.commit()
        # Retrieve the ID of the inserted type
        row = cursor.execute("SELECT Id FROM ParameterTypes WHERE Type = ?;", [type])
        return row.fetchone()[0]

    def get_types(self):
        """Retrieve all parameter types from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM ParameterTypes;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_unit(self, unit):
        """Insert parameter unit into the database."""
        cursor = self.database.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO ParameterUnits (Unit) VALUES (:unit);",[unit]
        )
        self.database.commit()
        # Retrieve the ID of the inserted unit
        row = cursor.execute("SELECT Id FROM ParameterUnits WHERE Unit = ?;", [unit])
        return row.fetchone()[0]

    def get_units(self):
        """Retrieve all parameter units from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM ParameterUnits;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_definition(self, data):
        """Insert parameter definition into the database."""
        cursor = self.database.cursor()
        # First try to insert or update to ensure all definitions are set
        cursor.execute(
            """INSERT INTO ParameterDefinitions (Definition, Comment) VALUES (:definition, :comment)
             ON CONFLICT(Definition)
             DO UPDATE SET Comment = :comment WHERE Definition = :definition;""",
            data
        )
        self.database.commit()
        # Retrieve the ID of the inserted definition
        row = cursor.execute("SELECT Id FROM ParameterDefinitions WHERE Definition = ?;", [data["definition"]])
        return row.fetchone()[0]

    def get_definitions(self):
        """Retrieve parameter definitions."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM ParameterDefinitions;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_field(self, data):
        """Insert parameter fields into the database."""
        cursor = self.database.cursor()
        # First try to insert or update to ensure all fields are set
        cursor.executemany(
            """INSERT INTO ParameterFields
             (Name, RefEngName, Size, Offset, Type, SourcePartition, DataStructure, Value, Definition, Unit, Description, Min, Max, LowBit, HighBit, Comment)
             VALUES
             (:name, :eng_name, :size, :offset, :type, :src_partition, :structure_id, :value, :definition, :unit, :description, :min, :max, :low_bit, :high_bit, :comment)
             ON CONFLICT(Name)
             DO UPDATE SET
             RefEngName = :eng_name,
             Size = :size,
             Offset = :offset,
             Type = :type,
             SourcePartition = :src_partition,
             DataStructure = :structure_id,
             Value = :value,
             Definition = :definition,
             Unit = :unit,
             Description = :description,
             Min = :min,
             Max = :max,
             LowBit = :low_bit,
             HighBit = :high_bit,
             Comment = :comment
             WHERE Name = :name;""",
            [data]
        )
        self.database.commit()