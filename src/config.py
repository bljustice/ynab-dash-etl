import os
from typing import Dict


class BaseConfig:
    """
    Base config for job
    """
    TESTING = False
    DEBUG = False
    YNAB_PERSONAL_TOKEN = os.environ['YNAB_PERSONAL_TOKEN']
    YNAB_BUDGET_ID = os.environ['YNAB_BUDGET_ID']


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
    pass


def build_config(env: str) -> Dict:
    """
    Used to build config object in ETL job
    """
    env_dict = vars(DevConfig) if env == 'development' else vars(ProdConfig)
    config_dict = {**env_dict, **{'ENV': env}}
    return config_dict
