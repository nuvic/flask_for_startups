#!/bin/bash

# Use: ./scripts/db_revision_autogen.sh "description_for_this_db_revision"
alembic -c migrations/alembic.ini -x db=dev revision --autogenerate -m $1 --rev-id=$(date '+%Y%m%d' -u)_$1