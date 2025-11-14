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
        cursor.executescript(sql)
        self.database.commit()

    def get_partitions(self):
        """Retrieve static partition list from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM PartitionList;")
        # Return a dictionary mapping partition names to their IDs
        return {r[1]: r[0] for r in row.fetchall()}

    def get_equipment_list(self):
        """Retrieve static equipment list from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM ViewEquipmentList;")
        # Return a dictionary mapping equipment names to their IDs
        return {r[1]: r[0] for r in row.fetchall()}

    def get_modules(self):
        """Retrieve static module list from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM Modules;")
        # Return a dictionary mapping module names to their IDs
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_structure(self, data):
        """Insert a data structure into the database."""
        cursor = self.database.cursor()
        cursor.execute(
            """INSERT INTO DataStructures (EngName, SourcePartition, SourceEquipment, Channel, MonitorPoint)
             VALUES (:name, :src_partition, NULL, NULL, NULL)
             ON CONFLICT(EngName)
             DO UPDATE SET SourcePartition = :src_partition WHERE EngName = :name;""",
            data
        )
        self.database.commit()
        # Retrieve the ID of the inserted structure
        row = cursor.execute(
            "SELECT Id FROM DataStructures WHERE EngName = ?;", [data["name"]])
        return row.fetchone()[0]

    def insert_structure_from_equipment(self, data):
        """Insert a data structure from equipment list into the database."""
        cursor = self.database.cursor()
        cursor.execute(
            """INSERT INTO DataStructures (EngName, SourcePartition, SourceEquipment, Channel, MonitorPoint)
             VALUES (:name, :src_partition, :src_equipment, :channel_id, :monitor_point)
             ON CONFLICT(EngName)
             DO UPDATE SET SourceEquipment = :src_equipment, Channel = :channel_id, MonitorPoint = :monitor_point WHERE EngName = :name;""",
            data
        )
        self.database.commit()

    def get_structure_id(self, name):
        """Retrieve data structure ID by name."""
        cursor = self.database.cursor()
        row = cursor.execute(
            "SELECT Id FROM DataStructures WHERE EngName = ?;", [name])
        result = row.fetchone()
        if result is not None:
            return result[0]
        return None

    def insert_type(self, type):
        """Insert parameter types into the database."""
        cursor = self.database.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO ParameterTypes (Type) VALUES (:type);", [
                type]
        )
        self.database.commit()
        # Retrieve the ID of the inserted type
        row = cursor.execute(
            "SELECT Id FROM ParameterTypes WHERE Type = ?;", [type])
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
            "INSERT OR IGNORE INTO ParameterUnits (Unit) VALUES (:unit);", [
                unit]
        )
        self.database.commit()
        # Retrieve the ID of the inserted unit
        row = cursor.execute(
            "SELECT Id FROM ParameterUnits WHERE Unit = ?;", [unit])
        return row.fetchone()[0]

    def get_units(self):
        """Retrieve all parameter units from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM ParameterUnits;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_enum_definition(self, data):
        """Insert parameter definition into the database."""
        cursor = self.database.cursor()
        # First try to insert or update to ensure all definitions are set
        cursor.execute(
            """INSERT INTO ParameterEnumDefinitions (Definition, Comment) VALUES (:definition, :comment)
             ON CONFLICT(Definition)
             DO UPDATE SET Comment = :comment WHERE Definition = :definition;""",
            data
        )
        self.database.commit()
        # Retrieve the ID of the inserted definition
        row = cursor.execute(
            "SELECT Id FROM ParameterEnumDefinitions WHERE Definition = ?;", [data["definition"]])
        return row.fetchone()[0]

    def get_enum_definitions(self):
        """Retrieve parameter definitions."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM ParameterEnumDefinitions;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_enum_value(self, data):
        """Insert parameter enum value into the database."""
        cursor = self.database.cursor()
        # First try to insert or update to ensure all values are set
        cursor.execute(
            """INSERT OR REPLACE INTO ParameterEnumValues (ParameterField, Value, Definition) VALUES (:field_id, :value, :definition_id);""",
            data
        )
        self.database.commit()

    def insert_field(self, data):
        """Insert parameter fields into the database."""
        cursor = self.database.cursor()
        # First try to insert or update to ensure all fields are set
        cursor.executemany(
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
            [data]
        )
        self.database.commit()
        # Retrieve the ID of the inserted field
        row = cursor.execute(
            "SELECT Id FROM ParameterFields WHERE Name = ?;", [data["name"]])
        return row.fetchone()[0]

    def get_channel_source(self, equipment: str, module: str):
        """Retrieve channel source mapping from the database."""
        cursor = self.database.cursor()
        eq_row = cursor.execute(
            "SELECT Id FROM Equipments WHERE Name = ?;", [equipment])
        eq_id = eq_row.fetchone()
        mod_row = cursor.execute(
            "SELECT Id FROM Modules WHERE Name = ?;", [module])
        mod_id = mod_row.fetchone()
        if eq_id is None or mod_id is None:
            return None
        return (eq_id[0], mod_id[0])

    def get_channel_directions(self):
        """Retrieve channel directions from the database."""
        cursor = self.database.cursor()
        row = cursor.execute("SELECT * FROM ChannelDirection;")
        return {r[1]: r[0] for r in row.fetchall()}

    def insert_channel(self, data):
        """Insert channel into the database."""
        cursor = self.database.cursor()
        cursor.execute(
            """INSERT INTO Channels
             (Id, Equipment, Module, Direction, DataStructure, Description)
             VALUES
             (:id, :equipment, :module, :direction, :data_structure, :desc)
             ON CONFLICT(Id, Equipment, Module)
             DO UPDATE SET
             Equipment = :equipment,
             Module = :module,
             Direction = :direction,
             DataStructure = :data_structure,
             Description = :desc
             WHERE Id = :id;""",
            data
        )
        self.database.commit()
