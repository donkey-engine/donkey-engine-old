#!/bin/bash
ALEMBIC_PATH="$(which alembic)"
if [ ! -f alembic.ini ]; then
    # alembic script should be run in directory with alembic.ini config file
    cd src/
fi
env PYTHONPATH=$(pwd)/../ ${ALEMBIC_PATH} upgrade heads
