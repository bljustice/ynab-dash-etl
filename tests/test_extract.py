import os
import unittest

from ynabdashetl.extract import BudgetExtractJob
from ynab.budgets import Budgets


class TestBudgets(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """"
        """
        token = os.environ['YNAB_PERSONAL_TOKEN']

        cls.job = BudgetExtractJob()
        cls.client = Budgets(token)

    def test_add_snapshot_date(self):
        """
        """
        result = self.job.add_snapshot_date()
        self.assertIn('start_date', result)
        self.assertIn('end_date', result)

    def test_get_budget_info(self):
        """
        """
        result = self.job.get_budget_info(self.client)
        self.assertIn('data', result)
        self.assertIn('start_date', result)
        self.assertIn('end_date', result)
