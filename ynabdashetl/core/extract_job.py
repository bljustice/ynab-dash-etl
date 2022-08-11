import logging
import datetime
from typing import Dict, Union

from ynab.accounts import Accounts
from ynab.budgets import Budgets
from ynab.categories import Categories
from ynab.transactions import Transactions

from ynabdashetl.core.config import build_config
from ynabdashetl.core.helpers import get_env

NAME = 'ynab.etl.extractjob'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(NAME)


class ExtractJob:

    name = NAME
    config = build_config(get_env())
    # budget_folder = os.path.join(os.getcwd(), 'data/budgets/extracts')

    def __init__(self, extract_name: str, extract_date: str) -> None:

        self.extract_name = extract_name
        self.extract_date = extract_date

    @property
    def ynab_client(self) -> Union[Accounts, Budgets, Categories, Transactions]:

        client_dict = {
            'accounts': Accounts,
            'budgets': Budgets,
            'categories': Categories,
            'transactions': Transactions, 
        }
        return client_dict[self.extract_name]

    def add_snapshot_date(self) -> Dict[str, str]:
        """
        Simply gets today's date and tomorrow's date and
        puts them into a dictionary to combine with budget data.
        """
        start_datetime = datetime.strptime(self.extract_date)
        end_datetime = start_datetime + datetime.timedelta(days=1)

        start_date, end_date = map(lambda x: x.strftime('%Y-%m-%d'), [start_datetime, end_datetime])

        return {
            'start_date': start_date,
            'end_date': end_date,
        }
