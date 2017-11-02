#!/bin/bash

DIR=`dirname $0`

while ! nc -z postgres 5432
do
    sleep 1
    echo 'Waiting for PostgreSQL'
done

#while [ true ]
#do
#    COUNT="$(psql -U camper -h postgres -c \"COPY(SELECT COUNT(*) FROM pg_tables WHERE tablename='values_value'\") TO STDOUT)"
#    if ! [ "$COUNT" -eq "0" ]
#    then
#        break
#    else
#        echo 'Wating for migrations to complete'
#        sleep 1
#    fi
#done

#psql -U camper -h postgres -c ""
#for CMD in ${@}
#do
#    $MANAGE ${CMD}
#done

exec $DIR/$1.sh

