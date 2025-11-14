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
from defusedxml.minidom import parse
from database import Database


class GildaXml:
    """GILDA XML parser class."""

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
        return set(s).issubset({'0', '1'})

    def parse(self, file=None):
        """Parse a GILDA XML file and insert data into the database."""
        if file is None:
            return
        # Get static partition mapping from the database
        partitions = self.database.get_partitions()
        equipments = self.database.get_equipment_list()
        types = self.database.get_types()
        units = self.database.get_units()
        definitions = self.database.get_enum_definitions()

        try:
            # Parse the XML file
            document = parse(file)
            # Extract monitored data structures from equipment list
            equipment_list = document.getElementsByTagName("EquipementList")
            if len(equipment_list) > 0:
                equipment_list = equipment_list[0].getElementsByTagName(
                    "Equipement")
            for equ in equipment_list:
                eq_name = equ.getAttribute("Name")
                eq_id = equipments[eq_name]
                channels = equ.getElementsByTagName("Channel")
                for ch in channels:
                    ch_struct = ch.getAttribute("DataStructure")
                    ch_id = ch.getAttribute("ID")
                    ch_mp = int(ch.getAttribute("MonitorPoint"), 16)
                    struct_data = {
                        "name": ch_struct,
                        "src_partition": None,
                        "src_equipment": eq_id,
                        "channel_id": ch_id,
                        "monitor_point": ch_mp,
                    }
                    self.database.insert_structure_from_equipment(struct_data)

            # Extract structures and fields
            structures = document.getElementsByTagName("Structure")
            for struct in structures:
                # Handle data structure
                if struct.hasAttribute("EngName") and struct.hasAttribute("EmittedByPartition"):
                    eng_name = struct.getAttribute("EngName")
                    src_partition = partitions[struct.getAttribute(
                        "EmittedByPartition")]
                    struct_data = {
                        "name": eng_name,
                        "src_partition": src_partition,
                        "src_equipment": None,
                        "channel_id": None,
                        "monitor_point": None,
                    }
                    struct_id = self.database.insert_structure(struct_data)
                    # Handle fields associated with the structure
                    fields = struct.getElementsByTagName("Field")
                    for field in fields:
                        if field.hasAttribute("Name"):
                            field_data = {
                                "structure_id": struct_id,
                                "name": field.getAttribute("Name"),
                                "size": int(field.getAttribute("Size")),
                                "offset": int(field.getAttribute("Offset")),
                                "src_partition": src_partition,
                                "description": field.getAttribute("Description") if field.hasAttribute("Description") else None,
                                "min": None,
                                "max": None,
                                "low_bit": None,
                                "high_bit": None,
                                "comment": None,
                                "eng_name": None,
                            }
                            bits = field.getElementsByTagName("BitField")
                            if len(bits) > 0:
                                bitrange = bits[0]
                                if bitrange.hasAttribute("LowBit") and bitrange.hasAttribute("HighBit"):
                                    field_data["low_bit"] = bitrange.getAttribute(
                                        "LowBit")
                                    field_data["high_bit"] = bitrange.getAttribute(
                                        "HighBit")
                            # Process NonEnumerate types and units
                            # Populate types and units if not already present
                            non_enums = field.getElementsByTagName(
                                "NonEnumerate")
                            for ne in non_enums:
                                if ne.hasAttribute("Type"):
                                    type = ne.getAttribute("Type")
                                    if type not in types:
                                        # Insert new type into the database
                                        id = self.database.insert_type(type)
                                        types[type] = id

                                if ne.hasAttribute("Unit"):
                                    unit = ne.getAttribute("Unit")
                                    if unit not in units:
                                        # Insert new unit into the database
                                        id = self.database.insert_unit(unit)
                                        units[unit] = id
                                # Insert new parameter field into the database
                                field_data["eng_name"] = ne.getAttribute(
                                    "RefEngName")
                                field_data["unit"] = units[unit]
                                field_data["type"] = types[type]
                                # Get optional limits for parameter
                                dom = ne.getElementsByTagName("UsageDomain")
                                if len(dom) > 0:
                                    usage = dom[0]
                                    if usage.hasAttribute("Min") and usage.hasAttribute("Max"):
                                        field_data["min"] = usage.getAttribute(
                                            'Min')
                                        field_data["max"] = usage.getAttribute(
                                            'Max')
                                # Finally insert the field
                                self.database.insert_field(field_data)

                            # Process Enumerate types
                            enums = field.getElementsByTagName("Enumerate")
                            # Both Enumerate and NonEnumerate should not be present simultaneously
                            if len(enums) > 0:
                                if len(non_enums) > 0:
                                    raise ValueError(
                                        f"Field '{field.getAttribute('Name')}' has both Enumerate and NonEnumerate definitions.")

                                field_data["unit"] = units["unitless"]
                                field_data["type"] = types["enum"]
                                field_id = self.database.insert_field(
                                    field_data)

                                for en in enums:
                                    if en.hasAttribute("Value") and en.hasAttribute("Definition"):
                                        definition = en.getAttribute(
                                            "Definition")
                                        comment = en.getAttribute(
                                            "Comments") if en.hasAttribute("Comments") else ""
                                        if definition not in definitions:
                                            data = {
                                                "definition": definition,
                                                "comment": comment
                                            }
                                            # Insert new definition into the database
                                            def_id = self.database.insert_enum_definition(
                                                data)
                                            definitions[definition] = def_id
                                        else:
                                            def_id = definitions[definition]

                                        # Validate that the enumeration value is a binary string
                                        if self.is_binary_string(en.getAttribute("Value")) is False:
                                            raise ValueError(
                                                f"Enumerate value '{en.getAttribute('Value')}' in field '{field.getAttribute('Name')}' is not a valid binary string.")
                                        enum_value = {
                                            "field_id": field_id,
                                            "definition_id": def_id,
                                            "value": int(
                                                en.getAttribute("Value"), base=2)
                                        }
                                        self.database.insert_enum_value(
                                            enum_value)

        except Exception as e:
            print(f"Error in '{file}': {e}")
            return

        return


class GildaChannelsXml(GildaXml):
    """GILDA Channels XML parser class."""

    def __init__(self, database_path: str):
        super().__init__(database_path)

    def parse(self, file=None):
        """Parse a GILDA Channels XML file and insert data into the database."""
        if file is None:
            return

        directions = self.database.get_channel_directions()

        try:
            # Parse the XML file
            document = parse(file)
            # Extract channel data
            channels = document.getElementsByTagName("Equipment_Channels")
            for ch in channels:
                # Source equipment name
                equipment = ch.getAttribute("Name")
                modules = ch.getElementsByTagName("Module")
                # Process each module within the equipment
                for mod in modules:
                    mod_name = mod.getAttribute("Name")
                    ids = self.database.get_channel_source(equipment, mod_name)
                    if ids is None:
                        raise ValueError(
                            f"Source equipment '{equipment}' or module '{mod_name}' not found in database.")
                    eq_id, mod_id = ids
                    # Each channel within a module is either from, to or between (inter) partitions
                    nodes = mod.getElementsByTagName("FromPartition")
                    nodes += mod.getElementsByTagName("ToPartition")
                    nodes += mod.getElementsByTagName("InterPartition")
                    for node in nodes:
                        ch = int(node.getAttribute(
                            "ChannelName").split("_")[1])
                        desc = node.getAttribute("Description")
                        direction = directions[node.tagName.replace(
                            "Partition", "")]
                        ds_id = None
                        if desc != "":
                            ds_id = self.database.get_structure_id(desc)

                        channel_data = {
                            "id": ch,
                            "equipment": eq_id,
                            "module": mod_id,
                            "direction": direction,
                            "data_structure": ds_id,
                            "desc": desc,
                        }
                        # print(channel_data)
                        self.database.insert_channel(channel_data)

        except Exception as e:
            print(f"Error in '{file}': {e}")
            return

        return
