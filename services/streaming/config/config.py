from configparser import ConfigParser
from services.streaming.config import DB_CONFIG


def config( filename=None, section='api' ):

    filename = filename if filename is not None else DB_CONFIG

    parser = ConfigParser()
    parser.read(filename)

    api_info = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            api_info[param[0]] = param[1]
    else:
        raise FileNotFoundError('Section {0} not found in the {1} file'.format(section, filename))

    return api_info
