import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from update_checker import UpdateChecker

class TestUpdateChecker(unittest.TestCase):
    @patch('requests.get')
    def test_check_for_updates_newer(self, mock_get):
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "0.3.0"}
        mock_get.return_value = mock_response

        # バージョン 0.2.0 に対して 0.3.0 は新しいはず
        with patch('update_checker.VERSION', '0.2.0'):
            result = UpdateChecker.check_for_updates()
            self.assertEqual(result, "0.3.0")

    @patch('requests.get')
    def test_check_for_updates_older(self, mock_get):
        # モックの設定
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"version": "0.1.0"}
        mock_get.return_value = mock_response

        # バージョン 0.2.0 に対して 0.1.0 は新しくない
        with patch('update_checker.VERSION', '0.2.0'):
            result = UpdateChecker.check_for_updates()
            self.assertIsNone(result)

    def test_version_comparison(self):
        self.assertTrue(UpdateChecker._is_newer("0.3.0", "0.2.0"))
        self.assertTrue(UpdateChecker._is_newer("1.0.0", "0.9.9"))
        self.assertFalse(UpdateChecker._is_newer("0.2.0", "0.2.0"))
        self.assertFalse(UpdateChecker._is_newer("0.1.0", "0.2.0"))

if __name__ == "__main__":
    unittest.main()
