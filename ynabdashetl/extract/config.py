import os
from typing import Dict


class BaseConfig(object):
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
    env_config = DevConfig if env == 'development' else ProdConfig

    token_dict = {
        'YNAB_PERSONAL_TOKEN': env_config.YNAB_PERSONAL_TOKEN,
        'YNAB_BUDGET_ID': env_config.YNAB_BUDGET_ID,
    }

    config_dict = {
        **{'ENV': 'env'},
        **vars(env_config),
        **token_dict,
    }

    return config_dict
