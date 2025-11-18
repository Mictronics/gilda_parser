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
            self.database = sqlite3.connect(database_path, isolation_level="DEFERRED")
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
        self.optimize()
        self.cursor.close()
        self.database.close()

    def close(self):
        """Close the database connection."""
        self.__exit__(None, None, None)

    def create(self, sql):
        """Create database schema."""
        self.database.execute("PRAGMA foreign_keys = OFF;")
        self.cursor.executescript(sql)
        self.database.commit()

    def get_partitions(self):
        """Retrieve static partition list from the database."""
        row = self.cursor.execute("SELECT * FROM PartitionList;")
        # Return a dictionary mapping partition names to their IDs
        return {r[1]: r[0] for r in row.fetchall()}

    def get_modules(self):
        """Retrieve static module list from the database."""
        row = self.cursor.execute("SELECT * FROM Modules;")
        # Return a dictionary mapping module names to their IDs
        return {r[1]: r[0] for r in row.fetchall()}

    def get_structures(self):
        """Retrieve all parameter units from the database."""
        row = self.cursor.execute("SELECT Id, EngName FROM DataStructures;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_structure(self, data):
        """Insert a data structure into the database."""
        self.cursor.execute(
            """INSERT INTO DataStructures (EngName, SourcePartition, Channel)
             VALUES (:name, :src_partition, :channel_id)
             ON CONFLICT(EngName)
             DO UPDATE SET SourcePartition = :src_partition WHERE EngName = :name;""",
            data,
        )
        self.database.commit()
        # Retrieve the ID of the inserted structure
        row = self.cursor.execute(
            "SELECT Id FROM DataStructures WHERE EngName = ?;", [data["name"]]
        )
        return row.fetchone()[0]

    def insert_type(self, type):
        """Insert parameter types into the database."""
        self.cursor.execute(
            "INSERT OR IGNORE INTO ParameterTypes (Type) VALUES (:type);", [type]
        )
        self.database.commit()
        # Retrieve the ID of the inserted type
        row = self.cursor.execute(
            "SELECT Id FROM ParameterTypes WHERE Type = ?;", [type]
        )
        return row.fetchone()[0]

    def get_types(self):
        """Retrieve all parameter types from the database."""
        row = self.cursor.execute("SELECT * FROM ParameterTypes;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_unit(self, unit):
        """Insert parameter unit into the database."""
        self.cursor.execute(
            "INSERT OR IGNORE INTO ParameterUnits (Unit) VALUES (:unit);", [unit]
        )
        self.database.commit()
        # Retrieve the ID of the inserted unit
        row = self.cursor.execute(
            "SELECT Id FROM ParameterUnits WHERE Unit = ?;", [unit]
        )
        return row.fetchone()[0]

    def get_units(self):
        """Retrieve all parameter units from the database."""
        row = self.cursor.execute("SELECT * FROM ParameterUnits;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_enum_definition(self, data):
        """Insert parameter definition into the database."""
        # First try to insert or update to ensure all definitions are set
        self.cursor.execute(
            """INSERT INTO ParameterEnumDefinitions (Definition, Comment) VALUES (:definition, :comment)
             ON CONFLICT(Definition)
             DO UPDATE SET Comment = :comment WHERE Definition = :definition;""",
            data,
        )
        self.database.commit()
        # Retrieve the ID of the inserted definition
        row = self.cursor.execute(
            "SELECT Id FROM ParameterEnumDefinitions WHERE Definition = ?;",
            [data["definition"]],
        )
        return row.fetchone()[0]

    def get_enum_definitions(self):
        """Retrieve parameter definitions."""
        row = self.cursor.execute("SELECT * FROM ParameterEnumDefinitions;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_enum_value(self, data):
        """Insert parameter enum value into the database."""
        # First try to insert or update to ensure all values are set
        self.cursor.execute(
            """INSERT OR REPLACE INTO ParameterEnumValues (ParameterField, Value, Definition) VALUES (:field_id, :value, :definition_id);""",
            data,
        )
        self.database.commit()

    def insert_field(self, data):
        """Insert parameter fields into the database."""
        # First try to insert or update to ensure all fields are set
        self.cursor.executemany(
            """INSERT INTO ParameterFields
             (Name, RefEngName, Size, Offset, Type, SourcePartition, DataStructure, Unit, Description, Min, Max, LowBit, HighBit)
             VALUES
             (:name, :eng_name, :size, :offset, :type, :src_partition, :structure_id, :unit, :description, :min, :max, :low_bit, :high_bit)
             ON CONFLICT(Name)
             DO UPDATE SET
             RefEngName = :eng_name,
             Size = :size,
             Offset = :offset,
             Type = :type,
             SourcePartition = :src_partition,
             DataStructure = :structure_id,
             Unit = :unit,
             Description = :description,
             Min = :min,
             Max = :max,
             LowBit = :low_bit,
             HighBit = :high_bit
             WHERE Name = :name;""",
            [data],
        )
        self.database.commit()
        # Retrieve the ID of the inserted field
        row = self.cursor.execute(
            "SELECT Id FROM ParameterFields WHERE Name = ?;", [data["name"]]
        )
        return row.fetchone()[0]

    def get_channel_source(self, equipment: str, module: str):
        """Retrieve channel source mapping from the database."""
        eq_row = self.cursor.execute(
            "SELECT Id FROM Equipments WHERE Name = ?;", [equipment]
        )
        eq_id = eq_row.fetchone()
        mod_row = self.cursor.execute(
            "SELECT Id FROM Modules WHERE Name = ?;", [module]
        )
        mod_id = mod_row.fetchone()
        if eq_id is None or mod_id is None:
            return None
        return (eq_id[0], mod_id[0])

    def get_channel_directions(self):
        """Retrieve channel directions from the database."""
        row = self.cursor.execute("SELECT * FROM ChannelDirection;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_channel(self, data):
        """Insert channel into the database."""
        self.cursor.execute(
            """INSERT INTO Channels
             (Id, Equipment, Module, Direction, Description)
             VALUES
             (:id, :equipment, :module, :direction, :desc)
             ON CONFLICT(Id, Equipment, Module)
             DO UPDATE SET
             Equipment = :equipment,
             Module = :module,
             Direction = :direction,
             Description = :desc
             WHERE Id = :id;""",
            data,
        )
        self.database.commit()

    def get_channel_id(self, desc):
        """Retrieve channel ID by name."""
        row = self.cursor.execute(
            "SELECT Id FROM Channels WHERE Description = ?;", [desc]
        )
        result = row.fetchone()
        if result is not None:
            return result[0]
        return None

    def get_fifo_parameter_fields(self):
        """Retrieve ARINC related parameter fields from the database."""
        row = self.cursor.execute("SELECT * FROM ViewFifoParameterFields;")
        return {
            r[1]: {"parameter_field_id": r[0], "fido_file": ""} for r in row.fetchall()
        }

    def insert_arinc_parameter(self, data):
        """Insert ARINC parameter into the database."""
        self.cursor.execute(
            """INSERT INTO ParameterArinc
             (ParameterFieldsId, Label, Name, Description, Type, Offset, Length, Unit, Min, Max, ScaleFactor)
             VALUES
             (:parameter_field_id, :label, :name, :desc, :type, :offset, :length, :unit, :min, :max, :scale)
             ON CONFLICT(Label, Name, ParameterFieldsId)
             DO UPDATE SET
             Description = :desc,
             Type = :type,
             Offset = :offset,
             Length = :length,
             Unit = :unit,
             Min = :min,
             Max = :max,
             ScaleFactor = :scale
             WHERE Label = :label AND Name = :name AND ParameterFieldsId = :parameter_field_id;""",
            data,
        )
        self.database.commit()

    def foreign_key_check(self) -> int:
        """
        Perform foreign key check.
        If the check fails a foreign key violation exists in the Gilda imported data.
        """
        rows = self.cursor.execute("PRAGMA foreign_key_check;")
        return len(rows.fetchall())

    def optimize(self):
        """Optimize the database."""
        self.cursor.execute("PRAGMA optimize;")
        self.database.commit()
        self.cursor.execute("VACUUM;")
