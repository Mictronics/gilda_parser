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

from database import Database


class GildaArinc:
    """GILDA ARINC parser class."""

    def __init__(self, database_path: str):
        # Initialize database connection
        self.database = Database(database_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close database connection
        self.database.close()

    def parse(self, arinc_conf: str):
        """Parse a GILDA ARINC Fido configuration and insert data into the database."""
        # Get FIFO parameter fields from the database
        fifo_to_file = self.database.get_fifo_parameter_fields()
        if arinc_conf is None and len(fifo_to_file) == 0:
            return

        path = os.path.dirname(arinc_conf)
        types = self.database.get_types()
        units = self.database.get_units()
        arinc_type_to_db_type = {
            "DIS": "discrete",
            "BIN": "binary",
            "BCD": "bcd",
            "TOR": "bool",
            "BNR": "binary",
        }
        try:
            # Read ARINC configuration file
            with open(arinc_conf, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    # Skip comments and empty lines
                    if not line.startswith("|") or line.strip() == "":
                        continue
                    parts = line.strip().split("|")
                    bus = parts[1].strip()
                    fido_file = parts[3].strip()
                    if bus in fifo_to_file:
                        fifo_to_file[bus]["fido_file"] = fido_file

            # Parse fido file for each FIFO parameter field
            for _fifo, file in fifo_to_file.items():
                if file["fido_file"] == "":
                    continue
                try:
                    with open(os.path.join(path, file["fido_file"]), "r", encoding="utf-8", errors="replace") as fido:
                        label = None
                        for line in fido:
                            # Check for begin of ARINC parameter definition
                            parts = line.strip().split("!")
                            parts = [p.strip() for p in parts]
                            if len(parts) < 18 or parts[0] == "#":
                                continue

                            if line.startswith("*") and parts[9] != "":
                                label = int(parts[3])

                            if parts[9] != "":
                                if parts[11] != "":
                                    type = arinc_type_to_db_type.get(
                                        parts[11])
                                    if type is None:
                                        raise ValueError(
                                            f"Parameter type not found: {parts[11]}")

                                    if type not in types:
                                        # Insert new type into the database
                                        id = self.database.insert_type(
                                            type)
                                        types[type] = id

                                if parts[14] != "":
                                    unit = parts[14]
                                    if unit == "S.U.":
                                        unit = "unitless"
                                    if unit not in units:
                                        # Insert new unit into the database
                                        id = self.database.insert_unit(
                                            unit)
                                        units[unit] = id

                                min_max = parts[15].split(" ")
                                if label is None:
                                    raise ValueError(
                                        f"Parameter name or label missing: {parts[10]}")
                                arinc_data = {
                                    "parameter_field_id": file["parameter_field_id"],
                                    "name": parts[9],
                                    "label": label,
                                    "type": types[type],
                                    "unit": units[unit],
                                    "desc": parts[10],
                                    "length": int(parts[12]),
                                    "offset": int(parts[13]),
                                    "min": float(min_max[0]),
                                    "max": float(min_max[1]),
                                    "scale": float(parts[16]),
                                }
                                self.database.insert_arinc_parameter(
                                    arinc_data)

                except Exception as e:
                    print(f"Error parsing FIDO file {file["fido_file"]}: {e}")

        except Exception as e:
            print(f"Error parsing ARINC file {arinc_conf}: {e}")
