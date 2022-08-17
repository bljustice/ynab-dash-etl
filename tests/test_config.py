import os
import unittest

from ynabdashetl.core.config import build_config


class ConfigTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """"
        """
        cls.config = build_config('development')

    def test_build_config(self):
 
        self.assertIn('YNAB_PERSONAL_TOKEN', dir(self.config))
        self.assertIn('YNAB_BUDGET_ID', dir(self.config))
        self.assertEqual(self.config.DEBUG, True)
