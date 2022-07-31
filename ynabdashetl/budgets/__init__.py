import os
import json
import logging
import datetime
import pandas as pd
from typing import Dict

from ynab.budgets import Budgets

from ynabdashetl.budgets.config import build_config
from ynabdashetl.budgets.helpers import get_env

NAME = 'ynab.etl.budgetjob'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(NAME)


class BudgetJob:

    name = NAME
    config = build_config(get_env())
    budget_folder = os.path.join(os.getcwd(), 'data/budgets')

    def get_budget_info(self, client: Budgets) -> Dict:
        """
        Use YNAB budget client to extract budget
        info.
        """

        budget_id = self.config['YNAB_BUDGET_ID']
        log.info('Getting budget data')
        budget_info = client.get_budget_by_id(budget_id)
        log.info('Got budget info successfully')
        
        # add snapshot date to budget data
        log.info('Adding snapshot dates to data')
        final_budget_dict = {
            **BudgetJob.add_snapshot_date(),
            **budget_info
        }

        log.info('Extracted all data successfully')
        return final_budget_dict

    @staticmethod
    def add_snapshot_date() -> Dict:
        """
        Simply gets today's date and tomorrow's date and
        puts them into a dictionary to combine with budget data.
        """
        start_datetime = datetime.date.today()
        end_datetime = start_datetime + datetime.timedelta(days=1)

        start_date = start_datetime.strftime('%Y-%m-%d')
        end_date = end_datetime.strftime('%Y-%m-%d')

        return {
            'start_date': start_date,
            'end_date': end_date,
        }

    @staticmethod
    def parse_budget_response(json_response: Dict) -> Dict:
        """
        Parse budget API response
        """
        return json_response['data']

    @staticmethod
    def to_dataframe(budget_info: Dict) -> pd.core.frame.DataFrame:
        """
        Converts json response into pandas dataframe
        """
        return pd.DataFrame(budget_info)

    def run(self) -> Dict:
        """
        Includes all code to complete ETL
        """
       
        log.info('Starting job')
        token = self.config['YNAB_PERSONAL_TOKEN']

        log.info('Getting budget info')
        client = Budgets(token)
        budget_info = self.get_budget_info(client)

        log.info('Writing json to file')
        write_filename = '.'.join([datetime.date.strftime(datetime.date.today(), '%Y-%m-%d'), 'json'])
        write_file_location = os.path.join(self.budget_folder, write_filename)
        with open(write_file_location, 'w') as f:
            json.dump(budget_info, f)

        log.info('Job complete')
        return True
