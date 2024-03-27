import unittest
from unittest.mock import patch
import logging

from quokkakit.lambdas.quokka import lambda_handler

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()

class LambdaHandlerTestCase(unittest.TestCase):
    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    @patch('utils.common.putNoteItem', return_value={'id': 1, 'content': 'New note'})
    def test_post_method_with_username(self, mock_put_note_item):
        event = {'body': '{"query":{"username":"john"},"method":"POST","body":{"username":"nk","content":"test"}}'}
        
        mock_put_note_item.return_value = {'username': 'nk', 'content': 'test'}
        expected_data = {'httpCode': 200, 'data': {'username': 'nk', 'content': 'test'}}

        response = lambda_handler(event, {})
        
        self.assertEqual(response, expected_data)

    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    @patch('utils.common.putNoteItem', return_value={'id': 1, 'content': 'New note'})
    def test_post_method_without_username(self, mock_put_note_item):
        event = {'body': '{"query":{"username":"john"},"method":"POST","body":{"username":"","content":"test"}}'}

        mock_put_note_item.return_value = {'username': 'nk', 'content': 'test'}
        expected_data = {'body': {'error': 'Method POST, Body missing fields'}, 'statusCode': 400}

        response = lambda_handler(event, {})
        self.assertEqual(response, expected_data)

    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    @patch('utils.common.putNoteItem', return_value={'id': 1, 'content': 'New note'})
    def test_post_method_without_content(self, mock_put_note_item):
        event = {'body': '{"query":{"username":"john"},"method":"POST","body":{"username":"nk","content":""}}'}

        mock_put_note_item.return_value = {'username': 'nk', 'content': 'test'}
        expected_data = {'body': {'error': 'Method POST, Body missing fields'}, 'statusCode': 400}

        response = lambda_handler(event, {})
        self.assertEqual(response, expected_data)

    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    @patch('utils.common.putNoteItem', return_value={'id': 1, 'content': 'New note'})
    def test_outof_method(self, mock_put_note_item):
        event = {'body': '{"query":{"username":"john"},"method":"PATCH","body":{"username":"nk","content":"test"}}'}

        mock_put_note_item.return_value = {'username': 'nk', 'content': 'test'}
        expected_data = {'body': {'error': 'Nothing'}, 'statusCode': 400}

        response = lambda_handler(event, {})
        self.assertEqual(response, expected_data)

    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    @patch('utils.common.queryPaginationByUsername', return_value=[{"username": "nk", "content": "test"}])
    @patch('utils.common.scanAllPagination', return_value=[{"username": "nk", "content": "test"}])
    def test_get_method_with_username(self, mock_get_scan_all, mock_get_note_by_username ):
        event = {'body': '{"query":{"username":"john"},"method":"GET"}'}

        expected_data = {'data': [{'username': 'nk', 'content': 'test'}], 'httpCode': 200}

        response = lambda_handler(event, {})
        self.assertEqual(response, expected_data)
        mock_get_scan_all.assert_not_called()

    @patch.dict('os.environ', {'NoteItemsTable': 'NoteItemsTable'})
    @patch('utils.common.queryPaginationByUsername', return_value=[{"username": "nk", "content": "test"}])
    @patch('utils.common.scanAllPagination', return_value=[{"username": "nk", "content": "test"}])
    def test_get_method_with_get_all(self, mock_get_scan_all, mock_get_note_by_username ):
        event = {'body': '{"query":{"username":""},"method":"GET"}'}

        expected_data = {'data': [{'username': 'nk', 'content': 'test'}], 'httpCode': 200}

        response = lambda_handler(event, {})
        self.assertEqual(response, expected_data)
        mock_get_note_by_username.assert_not_called()

if __name__ == '__main__':
    unittest.main()