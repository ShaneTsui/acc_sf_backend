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
