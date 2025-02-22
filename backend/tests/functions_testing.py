import unittest
from unittest.mock import patch, MagicMock
from functions import store_api_key, get_api_key
from google import genai


class TestFunctions(unittest.TestCase):
    
    @patch('functions.db')
    
    def test_store_api_key_success(self, mock_db):
        fake_doc_ref = MagicMock()
        fake_collection = MagicMock()
        fake_collection.document.return_value = fake_doc_ref
        mock_db.collection.return_value = fake_collection
        
        
        result = store_api_key('AIzaSyDsAMSEAXzkrDTrR-jn8HyTHh-wxrpHKPo')
        
        fake_doc_ref.set.assert_called_once_with({"api_key": "AIzaSyDsAMSEAXzkrDTrR-jn8HyTHh-wxrpHKPo"})
        
        # return 0 if it succeeds
        self.assertEqual(result, 0)
        
    @patch('functions.db')
    def test_store_api_key_failure(self, mock_db):
        fake_doc_ref = MagicMock()
        fake_doc_ref.set.side_effect = Exception("Write failed")
        fake_collection = MagicMock()
        fake_collection.document.return_value = fake_doc_ref
        mock_db.collection.return_value = fake_collection

        # return -1 if it fails
        result = store_api_key("sk-testkey")
        fake_doc_ref.set.assert_called_once_with({"api_key": "sk-testkey"})
        self.assertEqual(result, -1)
        
    @patch('functions.db')
    def test_get_api_key_success(self, mock_db):
        
        # Fake document that exists with an API key
        fake_doc = MagicMock()
        fake_doc.exists = True
        fake_doc.to_dict.return_value = {"api_key": "sk-testkey"}
        fake_doc_ref = MagicMock()
        fake_doc_ref.get.return_value = fake_doc
        fake_collection = MagicMock()
        fake_collection.document.return_value = fake_doc_ref
        mock_db.collection.return_value = fake_collection

        # Call get_api_key and check if returns correct API key
        result = get_api_key()
        fake_doc_ref.get.assert_called_once()
        self.assertEqual(result.get("api_key"), "sk-testkey")

    @patch('functions.db')
    def test_get_api_key_nonexistent(self, mock_db):
        # Simulate a document that does not exist
        fake_doc = MagicMock()
        fake_doc.exists = False
        fake_doc_ref = MagicMock()
        fake_doc_ref.get.return_value = fake_doc
        fake_collection = MagicMock()
        fake_collection.document.return_value = fake_doc_ref
        mock_db.collection.return_value = fake_collection

        # When the document doesn't exist, get_api_key should return None
        result = get_api_key()
        fake_doc_ref.get.assert_called_once()
        self.assertEqual(result, -1)

    @patch('functions.db')
    def test_get_api_key_failure(self, mock_db):
        # Simulate an exception being raised when calling .get()
        fake_doc_ref = MagicMock()
        fake_doc_ref.get.side_effect = Exception("Read failed")
        fake_collection = MagicMock()
        fake_collection.document.return_value = fake_doc_ref
        mock_db.collection.return_value = fake_collection

        # get_api_key should catch the exception and return -1
        result = get_api_key()
        fake_doc_ref.get.assert_called_once()
        self.assertEqual(result, -1)

if __name__ == '__main__':
    unittest.main()