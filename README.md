### Set up

- Copy `config-example.py` to `instance/config.py` and adjust the config variables for your environment.
- Create a new Postgres database with the name used in `SQLALCHEMY_DATABASE_URI` in the config file.
The app might work with older versions of PostgreSQL.
- Install the requirements from `requirements.txt`. If you are setting up a development environment, install
`requirements-dev.txt` too.

### Initialize Database
- Create a new Postgres database for the name used in `SQLALCHEMY_DATABASE_URI` in the config file.
- Run `./manage init-db` to create the database tables from the defined models in `api`. 

### Inserting Data into Database
- After initializing the database with `./manage init-db`.
- Download 3 data .csv files from Box "Oceans 1876/data/Oct18_speciesAndEnvironmentInfo" https://uofi.app.box.com/folder/124569566432.
- In your local oceans-1876 root directory, create a data folder and put the data files in there.
- Set `rootPath` and `dataPath` variables in `insertIntoDB.py`.
- Set `engine = create_engine('postgresql://username:password@host:port/database')` in `insertIntoDB.py`.
- For example: `engine = create_engine('postgresql://postgres:pw123@localhost:5432/oceans-1876')` in `insertIntoDB.py`.
- Run `python3 insertIntoData.py` to insert the data into the database.


### Use Flask

`./manage`  script is a wrapper for Flask cli, which handles some of the environment variable for Flask.
All arguments passed to `./manage` get passed to `flask` command directly. This script accepts two flags:
`-h` shows help and `-d` calls `flask` with development variables.

In order to run the server in development mode, call `./manage -d run`.
