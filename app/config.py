import os

from dotenv import find_dotenv, load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)


class Settings:
    CSRF_ENABLED: bool = True
    DEBUG: bool = False
    TESTING: bool = False
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    DATABASE_URL: str = os.environ["DATABASE_URL"] + "/acc_sf"
    # DATABASE_URL: str = os.environ["DATABASE_URL"].replace(
    #     "postgres://", "postgresql://", 1
    # )  # Hack: to fix heroku postgresql issue, see https://stackoverflow.com/a/66787229
