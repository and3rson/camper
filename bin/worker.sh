#!/bin/bash

DIR=`dirname $0`
MANAGE="python $DIR/../manage.py"

$MANAGE migrate
$MANAGE worker

