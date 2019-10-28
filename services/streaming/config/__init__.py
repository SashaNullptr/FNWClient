import os

ROOT_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
DB_CONFIG = os.path.join(ROOT_DIR, 'api.ini')

from .config import config
