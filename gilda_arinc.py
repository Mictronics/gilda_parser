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
import re
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

    def is_binary_string(self, s):
        """Check if a string is a binary representation (only '0' and '1')."""
        return set(s).issubset({"0", "1"})

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
                        # Label and offset are needed for linking ARINC discrete values to parameter
                        label = None
                        offset = None
                        for line in fido:
                            # Check for begin of ARINC parameter definition
                            parts = line.strip().split("!")
                            parts = [p.strip() for p in parts]
                            if len(parts) < 18 or parts[0] == "#":
                                continue

                            if line.startswith("*") and parts[9] != "":
                                # Store ARINC label if we got a new definition
                                label = int(parts[3])

                            if parts[9] != "":
                                # Handle parameter definitions within a label
                                if parts[11] != "":
                                    # Parameters should always have a type, except it's a discrete definition
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
                                    # We may also have a parameter unit
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
                                # Remember the offset for linking discrete definitions to a parameter
                                offset = int(parts[13])
                                arinc_data = {
                                    "parameter_field_id": file["parameter_field_id"],
                                    "name": parts[9],
                                    "label": label,
                                    "type": types[type],
                                    "unit": units[unit],
                                    "desc": parts[10],
                                    "length": int(parts[12]),
                                    "offset": offset,
                                    "min": float(min_max[0]),
                                    "max": float(min_max[1]),
                                    "scale": float(parts[16]),
                                }
                                # Store new ARINC parameter in database
                                self.database.insert_arinc_parameter(
                                    arinc_data)
                            # Handle ARINC discrete definition
                            # Fido field 10 is the only non-empty field.
                            elif parts[3] == "" and parts[10] != "":
                                # Separate the value in binary representation from its name
                                rgx = r"(?P<value>[01]+) (?P<name>.*)"
                                value, name = re.findall(
                                    rgx, parts[10], re.MULTILINE)[0]
                                # Ensure the value is in binary representation
                                if self.is_binary_string(value):
                                    # Convert to integer and store in database
                                    value = int(value, base=2)
                                    self.database.insert_arinc_discretes(
                                        {"value": value,
                                         "name": name,
                                         "label": label,
                                         "offset": offset,
                                         "parameter_field_id": file["parameter_field_id"]
                                         })

                except Exception as e:
                    print(f"Error parsing FIDO file {file["fido_file"]}: {e}")

        except Exception as e:
            print(f"Error parsing ARINC file {arinc_conf}: {e}")
