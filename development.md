# Development guide

This project uses FastAPI to provide an API for the data collected and created for Challenger Expedition project.

It uses PostgreSQL with PostGIS for database.

It is highly recommended to install `pre-commit` hooks by running `pre-commit install` before any development.
After installation, the hook will check for violation of typing and linting rules.
If a change that violates these rules is committed, its merge will get blocked via a GitHub Action (this can be bypassed if needed).
To test if there is any typing and linting issue, run `pre-commit run --all-files` from project root. You can also run `./script/lint.sh`.
If there is any issue, you can run `./scripts/lint.sh -f`, which tries to resolve the issue that can be solved automatically.
The rest must be resolved manually.

## API structure

Description of the main files and folders under `app` folder.

| file/folder        | description                                                                                                                                                                                                        |
|--------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| main.py            | The main entrypoint for the API. API app and its features are defined here.                                                                                                                                        |
| api/v1/endpoints/* | Functions that process requests/responses of endpoints                                                                                                                                                             |
| api/v1/router.py   | Defines the routes                                                                                                                                                                                                 |
| api/deps.py        | FastAPI dependencies which are injected as an argument into endpoint functions as needed                                                                                                                           |
| core/config.py     | API configuration.                                                                                                                                                                                                 |
| models/*           | SQLAlchemy classes that set up the database tables                                                                                                                                                                 |
| schemas/*          | Pydantic schemas that are used for validation of the data passed in requests and responses.<br/>For data coming from the database, the schemas handle data exchange between the API and database (via SQLAlchemy). |
