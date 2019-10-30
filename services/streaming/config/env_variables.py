from os import environ

def collect_env_vars(*argv):

    vars = {}

    for arg in argv:
        val = environ.get(arg)
        key = val.lower()
        vars[val] = key

    return vars
