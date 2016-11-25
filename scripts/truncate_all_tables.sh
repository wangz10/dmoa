#!/bin/bash
DATABASE_NAME='euclid'
## Force drop all tables
mysql -u root -Nse 'show tables' $DATABASE_NAME | while read table; do mysql -u root -e "SET FOREIGN_KEY_CHECKS = 0; drop table $table" $DATABASE_NAME; done
## Restore the schema 
mysql -u root $DATABASE_NAME < euclid.schema.sql
## Transfer the `drugs_lincs` table and rename it
mysqldump -u root maaya0_SEP drugs_lincs \
| sed -e 's/`drugs_lincs`/`drug`/' \
| mysql -u root $DATABASE_NAME
