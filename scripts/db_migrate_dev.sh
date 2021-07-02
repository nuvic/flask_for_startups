#!/bin/bash

# Usage: ./scripts/db_migrate_dev.sh

db_name=$(grep DB_NAME .flaskenv | cut -d '=' -f2) # retrieves the key DB_NAME from .flaskenv

alembic -c migrations/alembic.ini -x db=dev upgrade head && \
    rm -f migrations/schema.sql && \
    pg_dump -s $db_name >> migrations/schema.sql && \
    echo "Updated migrations/schema.sql"