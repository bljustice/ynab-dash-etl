from unittest import TestCase, mock
from moto import mock_s3

from ynabdashetl.core import ExtractJob

@mock_s3
class CoreTests(TestCase):

    def setUp(self):

        self.extract_job = ExtractJob('transactions', '2022-08-17')

        # need to set up a fake bucket for mock_s3 to work
        self.extract_job.s3_client.create_bucket(
            Bucket='ynab',
            CreateBucketConfiguration={
                'LocationConstraint': self.extract_job.config.AWS_REGION_NAME
            }
        )

        self.mock_response = mock.Mock(status_code=200)
        self.mock_response.json.return_value = {
            "data": {
                "transactions": [
                    {
                        "id": "string",
                        "date": "string",
                        "amount": 0,
                        "memo": "string",
                        "cleared": "cleared",
                        "approved": True,
                        "flag_color": "red",
                        "account_id": "string",
                        "payee_id": "string",
                        "category_id": "string",
                        "transfer_account_id": "string",
                        "transfer_transaction_id": "string",
                        "matched_transaction_id": "string",
                        "import_id": "string",
                        "deleted": True,
                        "account_name": "string",
                        "payee_name": "string",
                        "category_name": "string",
                        "subtransactions": [
                            {
                                "id": "string",
                                "transaction_id": "string",
                                "amount": 0,
                                "memo": "string",
                                "payee_id": "string",
                                "payee_name": "string",
                                "category_id": "string",
                                "category_name": "string",
                                "transfer_account_id": "string",
                                "transfer_transaction_id": "string",
                                "deleted": True
                            }
                        ]
                    }
                ],
                "server_knowledge": 0,
            }
        }

    @mock.patch('requests.get')
    def test_run(self, mock_get):

        mock_get.return_value = self.mock_response
        job_result = self.extract_job.run()
        self.assertEqual(job_result, True)
