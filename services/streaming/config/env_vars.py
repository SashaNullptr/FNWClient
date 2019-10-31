from os import environ


def collect_env_vars(*argv):
    vars = {}
    for arg in argv:
        val = environ.get(arg)
        key = arg.lower()
        vars[key] = val
    return vars
