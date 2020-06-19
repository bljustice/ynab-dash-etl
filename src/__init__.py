from ynab.budgets import Budgets

from .config import build_config
from .helpers import get_env


class Job:

    config = build_config(get_env())

    def run(self):
        """
        Includes all code to complete ETL
        """
        token = self.config['YNAB_PERSONAL_TOKEN']
        budget_id = self.config['YNAB_BUDGET_ID']

        client = Budgets(token)
        budget_info = client.get_budget_by_id(budget_id)
