# Setup and Run

## Recommended Python Version

This project is currently developed and tested with Python 3.13.

On this machine, the recommended interpreter is:

```text
G:\python\python.exe
```

Python 3.14 is currently not recommended for this project because some dependencies may not install cleanly.

## Install Dependencies

Run:

```bash
G:\python\python.exe -m pip install -r requirements.txt
```

## Run the API

Start the development server with:

```bash
G:\python\python.exe -m uvicorn app.main:app --reload
```

The API will then be available at:

```text
http://127.0.0.1:8000
```

Useful endpoints:

- `/`
- `/health`
- `/heroes`
- `/docs`

## Run Tests

Run:

```bash
G:\python\python.exe -m pytest
```

## Import Hero Data

Run:

```bash
G:\python\python.exe scripts/import_heroes.py
```

This script fetches public hero data from the Deadlock asset endpoint and imports it into the local database.

## Local Database

By default, the project uses a local SQLite database:

```text
sqlite:///./deadlock_meta.db
```

This is intended for lightweight local development.

## Planned PostgreSQL Support

The target production-style database for the project is PostgreSQL.

Later in development, the database URL can be switched by providing an environment variable:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/deadlock_meta
```

## Current Project Status

At the current stage:

- the FastAPI application is runnable
- the database models are defined
- SQLite tables are created automatically on startup
- initial API tests are passing
