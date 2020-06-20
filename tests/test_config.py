import unittest

from ynabdashetl.budgets.config import build_config


class ConfigTests(unittest.TestCase):

    def test_build_config(self):
 
        env = 'development'
        result = build_config(env)
        self.assertIn('ENV', result)
        self.assertIsInstance(result, dict)
