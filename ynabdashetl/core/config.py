import os

class BaseConfig(object):
    """
    Base config for job
    """

    TESTING = False
    DEBUG = False
    YNAB_PERSONAL_TOKEN = os.environ['YNAB_PERSONAL_TOKEN']
    YNAB_BUDGET_ID = os.environ['YNAB_BUDGET_ID']
    AWS_REGION_NAME = os.environ['AWS_REGION_NAME']
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


class DevConfig(BaseConfig):
    """
    Local config for job
    """

    TESTING = True
    DEBUG = True


class ProdConfig(BaseConfig):
    """
    Prod config for job
    """
    TESTING = False
    DEBUG = False


def build_config(env: str):
    """
    Used to build config object in ETL job
    """
    env_config = DevConfig if env == 'development' else ProdConfig
    return env_config
