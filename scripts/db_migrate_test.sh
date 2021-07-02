#!/bin/bash

# Usage: ./scripts/db_migrate_test.sh database_name

alembic -c migrations/alembic.ini -x db=test upgrade head