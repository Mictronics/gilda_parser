BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "DataStructures" (
	"Id"	INTEGER NOT NULL,
	"EngName"	TEXT NOT NULL UNIQUE,
	"SourcePartition"	INTEGER NOT NULL,
	PRIMARY KEY("Id" AUTOINCREMENT) ON CONFLICT IGNORE,
	FOREIGN KEY("SourcePartition") REFERENCES "PartitionList"("Id")
);
CREATE TABLE IF NOT EXISTS "EquipmentType" (
	"Id"	INTEGER NOT NULL,
	"Type"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "EthernetDefinitionList" (
	"Id"	INTEGER NOT NULL,
	"Equipment"	TEXT,
	"Ethernet"	TEXT,
	"Module"	INTEGER,
	PRIMARY KEY("Id"),
	FOREIGN KEY("Module") REFERENCES "Modules"("Id")
);
CREATE TABLE IF NOT EXISTS "Modules" (
	"Id"	INTEGER NOT NULL,
	"Name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "MonitoringPoint" (
	"Id"	INTEGER NOT NULL,
	"Type"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id")
);
CREATE TABLE IF NOT EXISTS "ParameterDefinitions" (
	"Id"	INTEGER NOT NULL,
	"Definition"	TEXT NOT NULL UNIQUE,
	"Comment"	TEXT,
	PRIMARY KEY("Id" AUTOINCREMENT) ON CONFLICT IGNORE
);
CREATE TABLE IF NOT EXISTS "ParameterFields" (
	"Id"	INTEGER NOT NULL,
	"Name"	TEXT NOT NULL UNIQUE,
	"RefEngName"	TEXT,
	"Size"	INTEGER NOT NULL,
	"Offset"	INTEGER NOT NULL,
	"Type"	INTEGER NOT NULL,
	"SourcePartition"	INTEGER NOT NULL,
	"DataStructure"	INTEGER NOT NULL,
	"Value"	INTEGER,
	"Definition"	INTEGER,
	"Unit"	INTEGER NOT NULL,
	"Description"	TEXT,
	PRIMARY KEY("Id" AUTOINCREMENT),
	FOREIGN KEY("DataStructure") REFERENCES "DataStructures"("Id"),
	FOREIGN KEY("Definition") REFERENCES "ParameterDefinitions"("Id"),
	FOREIGN KEY("SourcePartition") REFERENCES "PartitionList"("Id"),
	FOREIGN KEY("Type") REFERENCES "ParameterTypes"("Id"),
	FOREIGN KEY("Unit") REFERENCES "ParameterUnits"("Id")
);
CREATE TABLE IF NOT EXISTS "ParameterTypes" (
	"Id"	INTEGER NOT NULL,
	"Type"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id" AUTOINCREMENT) ON CONFLICT IGNORE
);
CREATE TABLE IF NOT EXISTS "ParameterUnits" (
	"Id"	INTEGER NOT NULL,
	"Unit"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Id" AUTOINCREMENT) ON CONFLICT IGNORE
);
CREATE TABLE IF NOT EXISTS "PartitionList" (
	"Id"	INTEGER NOT NULL,
	"Name"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("Id" AUTOINCREMENT)
);
INSERT INTO "EquipmentType" VALUES (1,'Partition');
INSERT INTO "EquipmentType" VALUES (2,'EquipmentDefinition');
INSERT INTO "EquipmentType" VALUES (3,'EquipmentInstallation');
INSERT INTO "EthernetDefinitionList" VALUES (1,'AMC1','193.0.161.111',1);
INSERT INTO "EthernetDefinitionList" VALUES (2,'AMC1','193.0.161.112',2);
INSERT INTO "EthernetDefinitionList" VALUES (3,'AMC2','193.0.161.121',1);
INSERT INTO "EthernetDefinitionList" VALUES (4,'AMC2','193.0.161.122',2);
INSERT INTO "EthernetDefinitionList" VALUES (5,'MFD1','193.0.161.211',3);
INSERT INTO "EthernetDefinitionList" VALUES (6,'MFD1','193.0.161.212',4);
INSERT INTO "EthernetDefinitionList" VALUES (7,'MFD2','193.0.161.221',3);
INSERT INTO "EthernetDefinitionList" VALUES (8,'MFD2','193.0.161.222',4);
INSERT INTO "EthernetDefinitionList" VALUES (9,'MFD3','193.0.161.231',3);
INSERT INTO "EthernetDefinitionList" VALUES (10,'MFD3','193.0.161.232',4);
INSERT INTO "EthernetDefinitionList" VALUES (11,'MFD4','193.0.161.241',3);
INSERT INTO "EthernetDefinitionList" VALUES (12,'MFD4','193.0.161.242',4);
INSERT INTO "EthernetDefinitionList" VALUES (13,'DTD','193.0.161.151',5);
INSERT INTO "EthernetDefinitionList" VALUES (14,'DTD_PC','193.0.161.50',5);
INSERT INTO "EthernetDefinitionList" VALUES (15,'IMT_PC','193.0.161.10',5);
INSERT INTO "EthernetDefinitionList" VALUES (16,'DMAU','193.0.161.55',5);
INSERT INTO "EthernetDefinitionList" VALUES (17,'WDTS1','193.0.161.151',5);
INSERT INTO "EthernetDefinitionList" VALUES (18,'STC','193.0.161.53',5);
INSERT INTO "Modules" VALUES (1,'ChA');
INSERT INTO "Modules" VALUES (2,'ChB');
INSERT INTO "Modules" VALUES (3,'SB1');
INSERT INTO "Modules" VALUES (4,'SB2');
INSERT INTO "Modules" VALUES (5,'N/A');
INSERT INTO "MonitoringPoint" VALUES (1,'Sender');
INSERT INTO "MonitoringPoint" VALUES (2,'Distribution');
INSERT INTO "MonitoringPoint" VALUES (3,'Sender+Distribution');
INSERT INTO "MonitoringPoint" VALUES (4,'Receiver');
INSERT INTO "MonitoringPoint" VALUES (5,'Sender+Receiver');
INSERT INTO "MonitoringPoint" VALUES (6,'Distribution+Receiver');
INSERT INTO "MonitoringPoint" VALUES (7,'All');
INSERT INTO "ParameterTypes" VALUES (1,'enum');
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
COMMIT;
