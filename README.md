### Set up

- Copy `config-example.py` to `instance/config.py` and adjust the config variables for your environment.
- Create a new Postgres database with the name used in `SQLALCHEMY_DATABASE_URI` in the config file.
The app might work with older versions of PostgreSQL.
- Install the requirements from `requirements.txt`. If you are setting up a development environment, install
`requirements-dev.txt` too.

### Initialize Database
- Create a new Postgres database for the name used in `SQLALCHEMY_DATABASE_URI` in the config file.
- Run `./manage init-db` to create the database tables from the defined models in `api`. 


### Use Flask

`./manage`  script is a wrapper for Flask cli, which handles some of the environment variable for Flask.
All arguments passed to `./manage` get passed to `flask` command directly. This script accepts two flags:
`-h` shows help and `-d` calls `flask` with development variables.

In order to run the server in development mode, call `./manage -d run`.
