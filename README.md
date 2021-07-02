# flask_for_startups

This project came out of Alex Krupp's article [Django for Startup Founders: A better software architecture for SaaS startups and consumer apps](https://alexkrupp.typepad.com/sensemaking/2021/06/django-for-startup-founders-a-better-software-architecture-for-saas-startups-and-consumer-apps.html). 

The main purpose of this structure is to allow your project to maximize the number of ideas and features you can test while making it easy to maintain development velocity.

Acknowledgements: Alex Krupp's repo [django_for_startups](https://github.com/Alex3917/django_for_startups)(based on above article) and Miguel Grinberg's [flask mega tutorial repo](https://github.com/miguelgrinberg/microblog).

## Instructions

### PostgreSQL setup

`sudo apt install postgresql postgresql-contrib`

Creating a new role:
```
sudo -u postgres psql
> create user your_user
> \password your_password
```

Creating a development database with necessary extensions:
```
sudo su postgres
createdb your_database_name
psql -d your_database_name
> grant all privileges on database your_database_name to your_user
> create extension if not exists pgcrypto with schema public;
> create extension if not exists "uuid-ossp" with schema public
```

(Optional: only if you want to run tests). Creating a test database with necessary extensions:
```
sudo su postgres
createdb your_test_database_name
psql -d your_test_database_name
> grant all privileges on database your_test_database_name to your_user
> create extension if not exists pgcrypto with schema public;
> create extension if not exists "uuid-ossp" with schema public
```

### Repo setup

* clone repo
* `python3 -m venv venv`
* activate virtual environment: `source venv/bin/activate`
* install requirements: `pip install -r requirements.txt`
* rename `.sample_flaskenv` to `.flaskenv` and update the relevant environment variables in `.flaskenv`
    * specifically: BASE_DIR, DEV_DATABASE_URI, DB_NAME, TEST_DATABASE_URI
* initialize the dev database: `./scripts/db_migrate_dev.sh`
* run server: `flask run`

### Updating db schema

* if you make changes to models.py and want alembic to auto generate the db migration: `./scripts/db_revision_autogen.sh "your_change_here"
* if you want to write your own changes: `./scripts/db_revision_manual.sh "your_change_here" and find the new migration file in `migrations/versions`

### Run tests

* if your test db needs to be migrated to latest schema: `./scripts/db_migrate_test.sh`
* `python -m pytest tests`

## Other details

* Why UUIDs as primary key?
  * see [brandur's article](https://brandur.org/nanoglyphs/026-ids) for a good analysis of UUID vs sequence IDs
  * instead of UUID4, you can use a sequential UUID like a [tuid](https://github.com/tanglebones/pg_tuid)
