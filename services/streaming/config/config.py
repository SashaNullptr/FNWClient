import os

from configparser import ConfigParser

ROOT_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
API_CONFIG = os.path.join(ROOT_DIR, 'credentials.ini')


def config(filename=None, section):

    filename = filename if filename is not None else API_CONFIG

    parser = ConfigParser()
    parser.read(filename)

    info = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            info[param[0]] = param[1]
    else:
        raise FileNotFoundError('Section {0} not found in the {1} file'.format(section, filename))

    return info
