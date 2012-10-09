#!/bin/bash


echo "The script you are running has basename `basename $0`, dirname `dirname $0`"
echo "The present working directory is `pwd`"

sudo pkill -f 'postgres: klp dbstatus'

origdir=`pwd`
SCRIPT_DIR=`dirname $0`

echo scriptdir




#/usr/sbin/apache2 -f ~/web/apache2.conf -k stop
DBNAME=$(basename $0 .sh)
OWNER=klp


echo droped db
sudo -u postgres dropdb ${DBNAME}

echo created db
sudo -u postgres createdb -O ${OWNER} -E UTF8 ${DBNAME}

echo creating dblink
sudo -u postgres psql -d ${DBNAME} -c "CREATE EXTENSION dblink"

# Create schema
echo creating schema
psql -U ${OWNER} -d ${DBNAME} -f ${SCRIPT_DIR}/${DBNAME}.sql 

echo creating csvs

# Load ${DBNAME}
python ${SCRIPT_DIR}/${DBNAME}.py
echo Finished creating csv files
echo Loading data into ${DBNAME}
sudo -u postgres psql -d ${DBNAME} -f ${SCRIPT_DIR}/load/load.sql
#updating timestamp
sudo -u postgres psql -d ${DBNAME} -c "insert into tb_statusinfo values(now());"
echo Finished Loading data
echo Db ready
