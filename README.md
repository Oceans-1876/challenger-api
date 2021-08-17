### Set up

- Make sure [Poetry](https://github.com/python-poetry/poetry) is available in your environment.
- Install the dependencies: `poetry install`.
- Create a PostgreSQL database and install PostGIS extension on it.
- Create `.env` file in project root (see `.env-example` for the available variables).
- Run the migrations to create the database tables: `./scripts/run_migrations.sh`.
- Run the dev server: `./scripts/run_dev_server.sh`.
- Run the dev email server: `./scripts/run_dev_email_server.sh`.

### Development

Before contributing to the code, make sure to install `pre-commit`: `pre-commit install`.

> If you need to run the `pre-commit` checks before committing your changes, run `pre-commit run --all-files`.

#### Scripts

| Script                  | Description                                                                                                                                                                 |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| create_migrations.sh    | Creates database migrations for new/changed models. Requires a message arg describing the changes.                                                                          |
| format.sh               | Runs a collection of linting and formatting tools and fix the issues that they can handle.  See the warning and error messages for issues that require manual intervention. |
| lint.sh                 | Runs a collection of linting and formatting tools without fixing the issues.                                                                                                |
| run_dev_email_server.sh | Starts a python email server that captures emails in the terminal.  Use the Email-related values in `.env-example` to use this server as the backend.                       |
| run_dev_server.sh       | Starts the API dev server.                                                                                                                                                  |
| run_migrations.sh       | Applies the migrations from `alembic/versions`.                                                                                                                             |
| run_tests.sh            | Runs the tests with `pytest` with coverage report.  It handles creation of a test database for `POSTGRES_TEST_DB` set in `.env`.                                            |
