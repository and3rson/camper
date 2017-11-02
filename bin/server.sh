#!/bin/bash

DIR=`dirname $0`
MANAGE="python $DIR/../manage.py"

$MANAGE runserver 0.0.0.0:9090

