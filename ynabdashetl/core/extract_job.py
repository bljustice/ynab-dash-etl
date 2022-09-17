import os
import boto3
import json
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

    def __init__(self, extract_name: str, extract_date: str) -> None:

        self.extract_name = extract_name
        self.extract_date = extract_date

    @property
    def s3_client(self) -> boto3.session.Session.client:

        return boto3.client(
            's3',
            region_name=self.config.AWS_REGION_NAME,
            aws_access_key_id=self.config.AWS_ACCESS_KEY,
            aws_secret_access_key=self.config.AWS_SECRET_ACCESS_KEY,
        )


    @property
    def ynab_api_method(self) -> Union[Accounts, Budgets, Categories, Transactions]:
        
        api_token = self.config.YNAB_PERSONAL_TOKEN
        client_dict = {
            'accounts': Accounts(api_token).get_accounts_by_budget_id,
            'budgets': Budgets(api_token).get_budget_by_id,
            'categories': Categories(api_token).get_categories_by_budget_id,
            'transactions': Transactions(api_token).get_transactions_by_budget_id,
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

    def put_json_to_s3(self, json_response, s3_key: str) -> bool:
        
        bucket_name = 'ynab'
        self.s3_client.put_object(
            Body=json.dumps(json_response),
            Bucket=bucket_name,
            Key=s3_key
        )
        return True


    def run(self) -> bool:

        log.info(f'Starting {self.extract_name} job for {self.extract_date}')

        params = {
            'budget_id': self.config.YNAB_BUDGET_ID,
        }

        if self.extract_name == 'transactions':
            params['since_date'] = self.extract_date

        log.info(f'Calling {self.extract_name} endpoint')
        api_response = self.ynab_api_method(**params)

        api_response_key = f'{self.extract_name}/{self.extract_date}.json'
        log.info(f'Writing json response to {api_response_key} in s3')
        self.put_json_to_s3(api_response, api_response_key)
        self.s3_client.close()
        
        log.info('Data written successfully.')
        log.info('Job complete')
        return True
