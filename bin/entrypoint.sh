#!/bin/bash

DIR=`dirname $0`
MANAGE="python $DIR/../manage.py"

while ! nc -z postgres 5432
    do sleep 1
    echo 'Waiting for PostgreSQL'
done

#psql -U camper -h postgres -c ""
$MANAGE migrate
$MANAGE ${@}
