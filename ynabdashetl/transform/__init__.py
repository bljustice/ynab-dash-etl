import os
import json
import logging
import pandas as pd

from datetime import datetime
from typing import Dict
from sqlalchemy import create_engine

from ynabdashetl.extract.config import build_config
from ynabdashetl.extract.helpers import get_env

NAME = 'ynab.etl.budgettransformjob'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(NAME)

class BudgetTransformJob:

    name = NAME
    config = build_config(get_env())
    budget_folder = os.path.join(os.getcwd(), 'data/budgets/extracts')

    def load_budget_json(self, filename) -> Dict:

        filepath = os.path.join(self.budget_folder, filename)
        json_content = json.loads(open(filepath).read())
        return json_content

    @staticmethod
    def _create_postgres_conn(dbname: str, port: int, username: str, password: str, host: str):

        engine_str = f'postgresql://{username}:{password}@{host}:{port}/{dbname}'

        conn = create_engine(engine_str)
        return conn

    def run(self) -> bool:

        log.info("Loading today's budget file.")
        todays_date = '.'.join([datetime.strftime(datetime.today(), '%Y-%m-%d'), 'json'])
        budget_json = self.load_budget_json(todays_date)

        log.info("Converting JSON into dataframe")
        budget_data = budget_json['data']['budget']
            
        # create transaction table
        transaction_df = pd.DataFrame(budget_data['transactions'])
    
        # create payee table
        payee_df = pd.DataFrame(budget_data['payees'])

        # create acccounts table
        accounts_df = pd.DataFrame(budget_data['accounts'])

        # create categories table
        categories_df = pd.DataFrame(budget_data['categories'])

        log.info('Creating postgres connection')
        conn_details = {
            'dbname': os.environ['dbname'],
            'port': os.environ['port'],
            'username': os.environ['username'],
            'password': os.environ['password'],
            'host': os.environ['host'],
        }
        conn = BudgetTransformJob._create_postgres_conn(**conn_details)

        log.info('Loading source tables into postgres')
        transaction_df.to_sql('ynab_transactions', conn, schema='warehouse', index=False)
        payee_df.to_sql('ynab_payees', conn, schema='warehouse', index=False)
        accounts_df.to_sql('ynab_accounts', conn, schema='warehouse', index=False)
        categories_df.to_sql('ynab_categories', conn, schema='warehouse', index=False)

        log.info("Job completed")
        return True
