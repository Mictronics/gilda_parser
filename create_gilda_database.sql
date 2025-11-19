BEGIN TRANSACTION;
DROP TABLE IF EXISTS "DataStructures";
CREATE TABLE "DataStructures" (
	"Id"	INTEGER NOT NULL,
	"EngName"	TEXT NOT NULL UNIQUE,
	"SourcePartition"	INTEGER,
	"Channel"	INTEGER,
	PRIMARY KEY("Id" AUTOINCREMENT),
	FOREIGN KEY("SourcePartition") REFERENCES "PartitionList"("Id")
);
DROP TABLE IF EXISTS "EthernetDefinitionList";
CREATE TABLE "EthernetDefinitionList" (
	"Id"	INTEGER NOT NULL,
	"Name"	TEXT,
	"Ethernet"	TEXT,
	"Equipment"	INTEGER,
	"Module"	INTEGER,
	PRIMARY KEY("Id"),
	FOREIGN KEY("Equipment") REFERENCES "Equipments"("Id")
	FOREIGN KEY("Module") REFERENCES "Modules"("Id")
);
DROP TABLE IF EXISTS "Equipments";
CREATE TABLE "Equipments" (
	"Id"	INTEGER NOT NULL,
	"Name"	TEXT NOT NULL,
	PRIMARY KEY("Id") ON CONFLICT IGNORE
);
DROP TABLE IF EXISTS "Modules";
CREATE TABLE "Modules" (
	"Id"	INTEGER NOT NULL,
	"Name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id")
);
DROP TABLE IF EXISTS "ParameterEnumDefinitions";
CREATE TABLE "ParameterEnumDefinitions" (
	"Id"	INTEGER NOT NULL,
	"Definition"	TEXT NOT NULL UNIQUE,
	"Comment"	TEXT,
	PRIMARY KEY("Id" AUTOINCREMENT) ON CONFLICT IGNORE
);
DROP TABLE IF EXISTS "ParameterEnumValues";
CREATE TABLE "ParameterEnumValues" (
	"ParameterField"	INTEGER NOT NULL,
	"Value"	INTEGER NOT NULL,
	"Definition"	INTEGER NOT NULL,
	PRIMARY KEY("ParameterField","Value","Definition"),
	FOREIGN KEY("Definition") REFERENCES "ParameterEnumDefinitions"("Id"),
	FOREIGN KEY("ParameterField") REFERENCES "ParameterFields"("Id")
);
DROP TABLE IF EXISTS "ParameterFields";
CREATE TABLE "ParameterFields" (
	"Id"	INTEGER NOT NULL,
	"Name"	TEXT NOT NULL UNIQUE,
	"RefEngName"	TEXT,
	"Size"	INTEGER NOT NULL,
	"Offset"	INTEGER NOT NULL,
	"Type"	INTEGER NOT NULL,
	"SourcePartition"	INTEGER NOT NULL,
	"DataStructure"	INTEGER NOT NULL,
	"Unit"	INTEGER NOT NULL,
	"Description"	TEXT,
	"Min"	NUMERIC,
	"Max"	NUMERIC,
	"LowBit"	INTEGER,
	"HighBit"	INTEGER,
	"Comment"	TEXT,
	PRIMARY KEY("Id" AUTOINCREMENT),
	FOREIGN KEY("DataStructure") REFERENCES "DataStructures"("Id"),
	FOREIGN KEY("SourcePartition") REFERENCES "PartitionList"("Id"),
	FOREIGN KEY("Type") REFERENCES "ParameterTypes"("Id"),
	FOREIGN KEY("Unit") REFERENCES "ParameterUnits"("Id")
);
DROP TABLE IF EXISTS "ParameterTypes";
CREATE TABLE "ParameterTypes" (
	"Id"	INTEGER NOT NULL,
	"Type"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id" AUTOINCREMENT) ON CONFLICT IGNORE
);
DROP TABLE IF EXISTS "ParameterUnits";
CREATE TABLE "ParameterUnits" (
	"Id"	INTEGER NOT NULL,
	"Unit"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id" AUTOINCREMENT) ON CONFLICT IGNORE
);
DROP TABLE IF EXISTS "PartitionList";
CREATE TABLE "PartitionList" (
	"Id"	INTEGER NOT NULL,
	"Name"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "ChannelDirection";
CREATE TABLE "ChannelDirection" (
	"Id"	INTEGER NOT NULL,
	"Direction"	TEXT NOT NULL,
	PRIMARY KEY("Id")
);
DROP TABLE IF EXISTS "Channels";
CREATE TABLE "Channels" (
	"Id"	INTEGER NOT NULL,
	"Equipment"	INTEGER NOT NULL,
	"Module"	INTEGER NOT NULL,
	"Direction"	INTEGER NOT NULL,
	"Description"	TEXT,
	PRIMARY KEY("Id","Equipment","Module"),
	FOREIGN KEY("Equipment") REFERENCES "EthernetDefinitionList"("Id"),
	FOREIGN KEY("Module") REFERENCES "Modules"("Id")
	FOREIGN KEY("Direction") REFERENCES "ChannelDirection"("Id")
);
DROP TABLE IF EXISTS "ParameterArinc";
CREATE TABLE "ParameterArinc" (
	"Label"	INTEGER NOT NULL,
	"Name"	TEXT NOT NULL,
	"Description"	TEXT,
	"ParameterFieldsId"	INTEGER NOT NULL,
	"Type"	INTEGER NOT NULL,
	"Offset"	INTEGER NOT NULL,
	"Length"	INTEGER NOT NULL,
	"Unit"	INTEGER,
	"Min"	REAL NOT NULL,
	"Max"	REAL NOT NULL,
	"ScaleFactor"	REAL NOT NULL,
	PRIMARY KEY("Label","Name","ParameterFieldsId"),
	FOREIGN KEY("ParameterFieldsId") REFERENCES "ParameterFields"("Id"),
	FOREIGN KEY("Type") REFERENCES "ParameterTypes"("Id"),
	FOREIGN KEY("Unit") REFERENCES "ParameterUnits"("Id")
);
INSERT INTO "Equipments" VALUES (1,'AMC');
INSERT INTO "Equipments" VALUES (2,'MFD');
INSERT INTO "Equipments" VALUES (3,'DTD');
INSERT INTO "Equipments" VALUES (4,'DTD_PC');
INSERT INTO "Equipments" VALUES (5,'IMT_PC');
INSERT INTO "Equipments" VALUES (6,'DMAU');
INSERT INTO "Equipments" VALUES (7,'WDTS1');
INSERT INTO "Equipments" VALUES (8,'STC');
INSERT INTO "Modules" VALUES (1,'ChA');
INSERT INTO "Modules" VALUES (2,'ChB');
INSERT INTO "Modules" VALUES (3,'Chx');
INSERT INTO "Modules" VALUES (4,'SB1');
INSERT INTO "Modules" VALUES (5,'SB2');
INSERT INTO "Modules" VALUES (6,'N/A');
INSERT INTO "ChannelDirection" VALUES (1,'From');
INSERT INTO "ChannelDirection" VALUES (2,'To');
INSERT INTO "ChannelDirection" VALUES (3,'Inter');
INSERT INTO "EthernetDefinitionList" VALUES (1,'AMC1A','193.0.161.111',1,1);
INSERT INTO "EthernetDefinitionList" VALUES (2,'AMC1B','193.0.161.112',1,2);
INSERT INTO "EthernetDefinitionList" VALUES (3,'AMC2A','193.0.161.121',1,1);
INSERT INTO "EthernetDefinitionList" VALUES (4,'AMC2B','193.0.161.122',1,2);
INSERT INTO "EthernetDefinitionList" VALUES (5,'MFD1SR1','193.0.161.211',2,3);
INSERT INTO "EthernetDefinitionList" VALUES (6,'MFD1SR2','193.0.161.212',2,4);
INSERT INTO "EthernetDefinitionList" VALUES (7,'MFD2SR1','193.0.161.221',2,3);
INSERT INTO "EthernetDefinitionList" VALUES (8,'MFD2SR2','193.0.161.222',2,4);
INSERT INTO "EthernetDefinitionList" VALUES (9,'MFD3SR1','193.0.161.231',2,3);
INSERT INTO "EthernetDefinitionList" VALUES (10,'MFD3SR2','193.0.161.232',2,4);
INSERT INTO "EthernetDefinitionList" VALUES (11,'MFD4SR1','193.0.161.241',2,3);
INSERT INTO "EthernetDefinitionList" VALUES (12,'MFD4SR2','193.0.161.242',2,4);
INSERT INTO "EthernetDefinitionList" VALUES (13,'DTD','193.0.161.151',3,5);
INSERT INTO "EthernetDefinitionList" VALUES (14,'DTD_PC','193.0.161.50',4,5);
INSERT INTO "EthernetDefinitionList" VALUES (15,'IMT_PC','193.0.161.10',5,5);
INSERT INTO "EthernetDefinitionList" VALUES (16,'DMAU','193.0.161.55',6,5);
INSERT INTO "EthernetDefinitionList" VALUES (17,'WDTS1','193.0.161.151',7,5);
INSERT INTO "EthernetDefinitionList" VALUES (18,'STC','193.0.161.53',8,5);
INSERT INTO "ParameterTypes" VALUES (1,'enum');
INSERT INTO "ParameterTypes" VALUES (2,'discrete');
INSERT INTO "ParameterTypes" VALUES (3,'binary');
INSERT INTO "ParameterTypes" VALUES (4,'bcd');
INSERT INTO "ParameterTypes" VALUES (5,'bool');
INSERT INTO "ParameterUnits" VALUES (1,'unitless');
INSERT INTO "PartitionList" VALUES (1,'N/A');
INSERT INTO "PartitionList" VALUES (2,'AFCS');
INSERT INTO "PartitionList" VALUES (3,'BSP');
INSERT INTO "PartitionList" VALUES (4,'CIRM');
INSERT INTO "PartitionList" VALUES (5,'DMAP');
INSERT INTO "PartitionList" VALUES (6,'DMS');
INSERT INTO "PartitionList" VALUES (7,'EFB');
INSERT INTO "PartitionList" VALUES (8,'ETHERNET');
INSERT INTO "PartitionList" VALUES (9,'HMI');
INSERT INTO "PartitionList" VALUES (10,'HTAWS');
INSERT INTO "PartitionList" VALUES (11,'IMT');
INSERT INTO "PartitionList" VALUES (12,'IO');
INSERT INTO "PartitionList" VALUES (13,'MAIN');
INSERT INTO "PartitionList" VALUES (14,'OPL');
INSERT INTO "PartitionList" VALUES (15,'MISSION_CM');
INSERT INTO "PartitionList" VALUES (16,'SR2_MAIN');
INSERT INTO "PartitionList" VALUES (17,'VMS_A');
INSERT INTO "PartitionList" VALUES (18,'VMS_C');
INSERT INTO "PartitionList" VALUES (19,'LOADER');
INSERT INTO "PartitionList" VALUES (20,'DTD');
INSERT INTO "PartitionList" VALUES (21,'ADAHRS');
DROP VIEW IF EXISTS ViewEquipmentList;
CREATE VIEW ViewEquipmentList AS
SELECT
  edf.Id AS Id,
  edf.Name AS Description,
  eq.Name AS Equipment,
  m.Name AS Module,
  edf.Ethernet AS IP
FROM EthernetDefinitionList edf
JOIN Equipments eq ON edf.Equipment = eq.Id
JOIN Modules m ON edf.Module = m.Id;
DROP VIEW IF EXISTS ViewParameterEnumValues;
CREATE VIEW ViewParameterEnumValues AS
SELECT
  pf.Id AS ParameterField,
  pf.Name AS Name,
  pev.Value AS Value,
  ped.Definition AS Definition,
  ped.Comment AS Comment
FROM ParameterEnumValues pev
JOIN ParameterFields pf ON pev.ParameterField = pf.Id
JOIN ParameterEnumDefinitions ped ON pev.Definition = ped.Id;
DROP VIEW IF EXISTS ViewChannels;
CREATE VIEW ViewChannels AS
SELECT
  ch.Id AS Id,
  eq.Name AS Equipment,
  m.Name AS Module,
  cd.Direction AS Direction,
  ch.Description AS Description
FROM Channels ch
LEFT JOIN EthernetDefinitionList edf ON ch.Equipment = edf.Id
LEFT JOIN Equipments eq ON edf.Equipment = eq.Id
LEFT JOIN Modules m ON edf.Module = m.Id
LEFT JOIN ChannelDirection cd ON ch.Direction = cd.Id;
DROP VIEW IF EXISTS ViewParameterFields;
CREATE VIEW ViewParameterFields AS
SELECT
  pf.Id AS Id,
  pf.Name AS Name,
  pf.RefEngName AS RefEngName,
  pf.Size AS Size,
  pf.Offset AS Offset,
  pt.Type AS Type,
  pl.Name AS SourcePartition,
  ds.EngName AS DataStructure,
  ds.Channel AS Channel,
  pu.Unit AS Unit,
  pf.Description AS Description,
  pf.Min AS Min,
  pf.Max AS Max,
  pf.LowBit AS LowBit,
  pf.HighBit AS HighBit,
  pf.Comment AS Comment
FROM ParameterFields pf
LEFT JOIN ParameterTypes pt ON pf.Type = pt.Id
LEFT JOIN ParameterUnits pu ON pf.Unit = pu.Id
LEFT JOIN PartitionList pl ON pf.SourcePartition = pl.Id
LEFT JOIN DataStructures ds ON pf.DataStructure = ds.Id;
DROP VIEW IF EXISTS ViewFifoParameterFields;
CREATE VIEW ViewFifoParameterFields AS
SELECT Id, RefEngName FROM ViewParameterFields WHERE Type='fifo' AND RefEngName NOT LIKE '' AND RefEngName NOT NULL;
DROP VIEW IF EXISTS ViewParameterArinc;
CREATE VIEW ViewParameterArinc AS
SELECT
  pa.Label AS Label,
  pa.Name AS Name,
  pa.Description AS Description,
  pf.RefEngName AS ParameterFieldName,
  pt.Type AS Type,
  pa.Offset AS Offset,
  pa.Length AS Length,
  pu.Unit AS Unit,
  pa.Min AS Min,
  pa.Max AS Max,
  pa.ScaleFactor AS ScaleFactor
FROM ParameterArinc pa
LEFT JOIN ParameterFields pf ON pa.ParameterFieldsId = pf.Id
LEFT JOIN ParameterTypes pt ON pa.Type = pt.Id
LEFT JOIN ParameterUnits pu ON pa.Unit = pu.Id;
COMMIT;
