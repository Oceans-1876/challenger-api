import json
import secrets

from app import PROJECT_ROOT


def create_env_file() -> None:
    env_file_path = PROJECT_ROOT / ".env"

    if env_file_path.exists():
        raise FileExistsError(
            "There is an existing .env file in project root. "
            "Please remove this file to generate a new one, or edit it manually."
        )

    server_url = (input("What is the host name? (must be a valid url)\n"),)
    print()

    ui_url = input("What is the frontend host name? (must be a valid url)\n")

    backend_cors_origins = [server_url, ui_url]
    print()

    postgres_server = input("What is the postgres server url (e.g. localhost:5432)?\n")
    print()

    postgres_user = input("What is the postgres user name?\n")
    print()

    postgres_password = input("What is the postgres password?\n")
    print()

    postgres_db = input("What is the postgres database name?\n")
    print()

    env_vars = {
        "DEBUG": "false",
        "SECRET_KEY": secrets.token_urlsafe(32),
        "BACKEND_CORS_ORIGINS": json.dumps(backend_cors_origins),
        "ENABLE_AUTH": "false",
        "SENTRY_DSN": "",
        "SERVER_HOST": server_url,
        "POSTGRES_SERVER": postgres_server,
        "POSTGRES_USER": postgres_user,
        "POSTGRES_PASSWORD": postgres_password,
        "POSTGRES_DB": postgres_db,
        "POSTGRES_TEST_DB": "tests_challenger_expedition",
    }

    env_vars_str = "\n".join([f"{k}={v}" for k, v in env_vars.items()])
    with open(env_file_path, "w") as f:
        f.write(env_vars_str)

    print(
        f"\n\nSuccessfully created .env file in {env_file_path} with the following content:\n"
    )
    print(env_vars_str)


if __name__ == "__main__":
    create_env_file()
