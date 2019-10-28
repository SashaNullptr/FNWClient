from configparser import ConfigParser

ROOT_DIR = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
DB_CONFIG = os.path.join(ROOT_DIR, 'api.ini')

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
