import os


def get_env() -> str:
    """
    Gets environment based on the ENV variable. Defaults to
    production if none is found.
    """
    env = os.environ.get('ENV')
    return env or 'production'
