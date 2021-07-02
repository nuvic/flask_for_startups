#!/bin/bash

# Use: ./scripts/db_revision_manual.sh "description_for_this_db_revision"
alembic -c migrations/alembic.ini revision -m $1 --rev-id=$(date '+%Y%m%d')_$1