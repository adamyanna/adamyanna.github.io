# PostgreSQL fundamental and operation

> 2018-10-25

Postgresql

2018-10-23 19:00:00 +0800

What is

object-ralational database management system - aka ORDMSSQL standard database features:

complex queriesforeign keystriggersupdatable viewstransactional integritymultiversion concurrency control extended features:

data typesfunctionsoperatorsaggregate functionsindex methodsprocedural languages Basic Command

\h: help for SQL syntax\?: PG command-line options\l: list all databases\c: connect another database\d: list all tables for database\d + <”table_name”>: describe table, view, sequence, or index\du: list all uesr\e: editor\conninfo: list current connection info Data type

number

typesizerangesmallint2byte-32768 ~ +32767integer4byte-2147483648 ~ +2147483647bigint8byte-9223372036854775808 ~ 9223372036854775807decimalvar*131072.*16383numericvar*131072.*16383real4byte*6double8byte*15serial4byte1 ~ 2147483647bigserial8byte1 ~ 922337203685477580 * String

typechar(size)character(size)varchar(size)character varying(size)text Date & Time

typetimestamptimestamp[utc]datetimetime[utc]interval Boolean

typevaluesizebooleantrue/false1byte Json

typedescjsontextual JOSN datajsonbbinary JOSN data other

typeuuidxml… Database

CREATE DATABASE db_name
DROP DATABASE db_name
Table

CREATE TABLE table_name(
column1 datatype,
column2 datatype,
column3 datatype,
.....
columnN datatype,
PRIMARY KEY( one or more columns )
);

DROP TABLE table_name;
Schema

A database contains one or more named schemas, which in turn contain tables. Schema contains other object like data types, functions, and operators. Schemas are not rigidly separated, a user can access objects in any of the schemas in the database they are connected to.

Contaion

tablesdata typesfunctionsoperators SQL syntax

1. INSERT

INSERT INTO TABLE_NAME (column1,...) VALUES (value1,...);
2. SELECT

SELECT "column1",... FROM "table_name";
3. UPDATE

UPDATE table_name
SET column1 = value1, ...
WHERE [condition]

UPDATE "table_name" set column1 = value1, ... WHERE condition = con_
