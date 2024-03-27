import unittest
from datetime import datetime
from unittest import mock
import boto3
import logging
from unittest.mock import MagicMock, patch

from quokkakit.lambdas.utils.common import getValueOfTimeEndDay, getValueOfTimeStartDay, putNoteItem, queryPaginationByUsername, scanAllPagination


logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

class TestTimeFunctions(unittest.TestCase):
    def test_getValueOfTimeStartDay(self):
        time = datetime(2024, 3, 27, 10, 30, 0)
        result = getValueOfTimeStartDay(time)
        expected = datetime(2024, 3, 27, 0, 0, 0).timestamp()
        self.assertEqual(result, expected)

    def test_getValueOfTimeEndDay(self):
        time = datetime(2024, 3, 27, 10, 30, 0)
        result = getValueOfTimeEndDay(time)
        expected = datetime(2024, 3, 27, 23, 59, 59).timestamp()
        self.assertEqual(result, expected)

# class TestDecimalEncoder(unittest.TestCase):
#     def test_decimalEncoder_float(self):
#         value = decimal.Decimal('10.123')
#         encoder = DecimalEncoder()
#         result = encoder.default(value)
#         expected = float(value)
#         self.assertEqual(result, expected)

#     def test_decimalEncoder_int(self):
#         value = decimal.Decimal('10.00')
#         encoder = DecimalEncoder()
#         result = encoder.default(value)
#         expected = int(value)
#         self.assertEqual(result, expected)


class TestHandler(unittest.TestCase):
    def handler(self):
        dynamodb = boto3.client('dynamodb')
        response = dynamodb.put_item(TableName='NoteTableTest', Item={'id': {'S': '1'}, 'content': {'S': 'Item 1'}, 'timestamp': {'N': 123}})
        return response

    @mock.patch("boto3.client")
    def test_handler(self, mock_client):
        mock_dynamodb = mock_client.return_value
        mock_dynamodb.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        response = self.handler()

        mock_client.assert_called_once_with('dynamodb')
        mock_dynamodb.put_item.assert_called_once_with(
            TableName='NoteTableTest',
            Item={'id': {'S': '1'}, 'content': {'S': 'Item 1'}, 'timestamp': {'N': 123}}
        )
        self.assertEqual(response, {'ResponseMetadata': {'HTTPStatusCode': 200}})


class DynampDbHandlerTestCase(unittest.TestCase):
    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    def setUp(self):
        # Set up the test environment
        self.dynamodb_mock = MagicMock()
        self.table_mock = MagicMock()
        self.dynamodb_mock.Table.return_value = self.table_mock
        self.original_dynamodb_resource = "NoteItemsTable"
        self.table_name = 'NoteItemsTable'
        self.original_table_name = "NoteItemsTable"

    def tearDown(self):
        # Restore the original values
        print()

    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    def test_input_dynamodb(self):
        self.table_mock.put_item.return_value = {'Attributes': {'id': 1, 'content': 'New note'}}
        
        item = putNoteItem({"username": "nk", "content": "content"}, self.table_mock)

        self.assertEqual(item['username'], 'nk')
        self.assertEqual(item['content'], 'content')

        self.assertTrue(bool(item['timestamp']))
        self.assertTrue(bool(item['id']))

    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    def test_get_pagination_dynamodb(self):
        ItemMock = {'id': 1, 'content': 'Note 1', "username": "nk"}
        self.table_mock.query.return_value = {'Items': [ItemMock,ItemMock]}
        items = queryPaginationByUsername(1, 'nk', self.table_mock)

        self.assertEqual(len(items), 2)
    
    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    def test_scan_all_dynamodb(self):
        ItemMock = {'id': 1, 'content': 'Note 1', "username": "nk"}
        self.table_mock.query.return_value = {'Items': [ItemMock,ItemMock]}
        items = scanAllPagination(1, self.table_mock)

        self.assertEqual(len(items), 2)
        


if __name__ == '__main__':
    unittest.main()