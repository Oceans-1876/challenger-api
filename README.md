# Set up

- After cloning the repo, set up `data` and `fonts` submodules:
  - `git submodule init`
  - `git submodule update`
- Make sure [Poetry](https://github.com/python-poetry/poetry) is available in your environment.
- Install the dependencies:
  - `poetry install`.
- Create a PostgreSQL (>= v13) database with the following extensions:
  - PostGIS (>= v3.1): `CREATE EXTENSION postgis`
  - pg_trgm (fuzzy string matching): `CREATE EXTENSION pg_trgm`
- Create `.env` file in project root (see `.env-example` for the available variables).
- Create tables and apply the migrations:
  - `poetry run ./scripts/migrations_forward.sh`.
- Import data into the tables:
  - `poetry run ./scripts/import_data.sh`.
- Run the dev server:
  - `poetry run ./scripts/run_dev_server.sh`.
- Run the dev email server (Optional, for auth- and user-related features. Not active at this point):
  - `poetry run ./scripts/run_dev_email_server.sh`.

## Development

Before contributing to the code, install `pre-commit`:
> `pre-commit install`.

> If you need to run the `pre-commit` checks before committing your changes, run `pre-commit run --all-files`.

### Database migrations

Migrations are managed by `alembic`. All revisions are in `alembic/versions`.

After adding new models or updating the existing ones, you need to create new migrations by running `poetry run ./scripts/migrations_create.sh "<Migration Message>"`.

To apply the new changes to an existing database, run `poetry run ./scripts/migrations_forward.sh`.

You can revert to a specific migration by running `poetry run ./scripts/migrations_reverse.sh <migration-id>`.
You can find the ID for each migration in its file in `alembic/versions`.

### Scripts

| Script                  | Description                                                                                                                                                                  |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| lint.sh                 | Runs a collection of linting and formatting tools. Use `-f` flag to fix the issues that can be handled automatically.                                                        |
| migrations_create.sh    | Creates database migrations for new/changed models. Requires a message arg describing the changes.                                                                           |
| migrations_forward.sh   | Forward migrations to the given revision. Default to `head` if a revision is not passed.                                                                                     |
| migrations_reverse.sh   | Reverse the migrations to the given revision.                                                                                                                                |
| import_data.sh          | Create the initial data.                                                                                                                                                     |
| run_dev_email_server.sh | Starts a python email server that captures emails in the terminal. Use the Email-related values in `.env-example` to use this server as the backend.                         |
| run_dev_server.sh       | Starts the API dev server.                                                                                                                                                   |
| run_tests.sh            | Runs the tests with `pytest` with coverage report. It handles creation of a test database for `POSTGRES_TEST_DB` set in `.env`.                                              |
| run_tests_coverage.sh   | Runs `run_tests.sh` script with coverage report.                                                                                                                             |
| build_docker.sh         | Builds the docker image.                                                                                                                                                     |

### Usage

You can see all the available endpoints at `/docs`.
