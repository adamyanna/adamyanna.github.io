---
title: PostgreSQL fundamental and operation
author: Teddy
date: 2018-10-23 19:00:00 +0800
categories: [体系结构-基础, 数据库系统概念]
tags: [Postgresql]
---


# What is
* object-ralational database management system - aka ORDMS
* SQL standard database

## features:
* complex queries
* foreign keys
* triggers
* updatable views
* transactional integrity
* multiversion concurrency control

## extended features:
* data types
* functions
* operators
* aggregate functions
* index methods
* procedural languages

***

# Basic Command
* \h: help for SQL syntax
* \?: PG command-line options
* \l: list all databases
* \c: connect another database
* \d: list all tables for database
* \d + <"table_name">: describe table, view, sequence, or index
* \du: list all uesr
* \e: editor
* \conninfo: list current connection info

# Data type
## number

| type | size | range |
| --------------- |----------- | ----------------- |
| smallint | 2byte | -32768 ~ +32767 |
| integer | 4byte | -2147483648 ~ +2147483647 |
| bigint | 8byte | -9223372036854775808 ~ 9223372036854775807 |
| decimal | var | \*131072.\*16383 |
| numeric | var | \*131072.\*16383 |
| real | 4byte | \*6 |
| double | 8byte | \*15 |
| serial | 4byte | 1 ~ 2147483647 |
| bigserial | 8byte | 1 ~ 922337203685477580 \* |

## String

| type |
|---------------|
|char(size)|		
|character(size)|
|varchar(size)|
|character varying(size)|
|text|

## Date & Time

| type |
|--------------|
|timestamp|
|timestamp[utc]|
|date|
|time|
|time[utc]|
|interval|

## Boolean

|type    	| value		| size |
|---------------|---------------|------|
|boolean    	|true/false		|1byte |

## Json

|type    	| desc |
|-----------|------------------|
|json    	|textual JOSN data |
|jsonb     |binary JOSN data |

## other

| type |
|-----|
|uuid|
|xml|
|...|

# Database

```SQL
CREATE DATABASE db_name
DROP DATABASE db_name
```

# Table

```SQL
CREATE TABLE table_name(  
   column1 datatype,  
   column2 datatype,  
   column3 datatype,  
   .....  
   columnN datatype,  
   PRIMARY KEY( one or more columns )  
);

DROP TABLE table_name;
```

# Schema

> A database contains one or more named schemas, which in turn contain tables.
> Schema contains other object like data types, functions, and operators.
> Schemas are not rigidly separated, a user can access objects in any of the schemas in the database they are connected to.

## Contaion

1. `tables`
2. `data types`
3. `functions`
4. `operators`

# SQL syntax

##### 1. INSERT

```SQL
INSERT INTO TABLE_NAME (column1,...) VALUES (value1,...);
```

##### 2. SELECT

```SQL
SELECT "column1",... FROM "table_name";
```

##### 3. UPDATE

```SQL
UPDATE table_name
SET column1 = value1, ...
WHERE [condition]

UPDATE "table_name" set column1 = value1, ... WHERE condition = con_value;
```

##### 4. DELETE

```SQL
DELETE FROM "table_name" WHERE condition = con_value;
```

##### 5. ORDER BY

```SQL
ORDER BY
WHERE

ORDER BY column1 ASC
ORDER BY column1 DESC
```

##### 6. GROUP BY

```SQL
GROUP BY sel_column1, ...
```

##### 7. HAVING

```SQL
GROUP BY sel_column1, ... HAVING [condition]
```
> use HAVING with GROUP BY syntax

##### 8. Condition

`AND`, `OR`, `AND & OR`, `NOT`, `LIKE`, `IN`, `NOT IN`, `BETWEEN`

##### 9. AND

```SQL
SELECT column1, ... FROM table_name WHERE [search_condition] AND [search_condition]
```

##### 10. OR

```SQL
SELECT column1, ... FROM table_name WHERE [search_condition] OR [search_condition]
```

##### 11. AND & OR

```SQL
SELECT column1, ... FROM table_name WHERE ([search_condition] AND [search_condition]) OR ([search_condition])
``` 

##### 12. NOT

```SQL
SELECT column1, ... FROM table_name WHERE [search_condition] NOT [condition]

SELECT column1, ... FROM table_name WHERE NOT [search_condition]
```

##### 13. LIKE

```SQL
SELECT column1, ... FROM table_name WHERE [search_condition] LIKE [condition]
```
> **Wildcard: %**

##### 14. IN

```SQL
SELECT column1, ... FROM table_name WHERE [search_condition] IN [condition]
```

##### 15. NOT IN

```SQL
SELECT column1, ... FROM table_name WHERE [search_condition] NOT IN [condition]
```

##### 16. BETWEEN

```SQL
SELECT column1, ... FROM table_name WHERE [search_condition] NOT BETWEEN [condition]
```

# Join

* INNER JOIN
* LEFT OUTER JOIN
* RIGHT OUTER JOIN
* FULL OUTER JOIN
* CROSS JOIN











