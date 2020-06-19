import logging
from typing import Dict

from ynab.budgets import Budgets

from budgets.config import build_config
from budgets.helpers import get_env

NAME = 'ynab.etl.budgetjob'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(NAME)


class BudgetJob:

    name = NAME
    config = build_config(get_env())

    def get_budget_info(self, client: Budgets) -> Dict:
        """
        Use YNAB budget client to extract budget
        info.
        """

        budget_id = self.config['YNAB_BUDGET_ID']
        budget_info = client.get_budget_by_id(budget_id)
        return budget_info

    def run(self):
        """
        Includes all code to complete ETL
        """
       
        log.info('Starting job')
        token = self.config['YNAB_PERSONAL_TOKEN']

        client = Budgets(token)
        log.info('Getting budget data')
        budget_info = self.get_budget_info(client)
        log.info('Got budget info successfully')
        log.info('Job complete')
        return budget_info
