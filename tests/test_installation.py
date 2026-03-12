import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from benchmark import ExcelBenchmark, ExcelNotInstalledError

class TestExcelInstallationCheck(unittest.TestCase):
    def setUp(self):
        self.bench = ExcelBenchmark(data_dir="test_data_check")

    @patch('win32com.client.Dispatch')
    def test_excel_not_installed_error(self, mock_dispatch):
        # Dispatchがエラーを投げるように設定
        mock_dispatch.side_effect = Exception("Invalid class string")
        
        with self.assertRaises(ExcelNotInstalledError):
            self.bench.create_instance()

    def test_urls_exist(self):
        self.assertIsNotNone(ExcelBenchmark.OFFICE_DOWNLOAD_URL)
        self.assertIsNotNone(ExcelBenchmark.LIBREOFFICE_DOWNLOAD_URL)

if __name__ == "__main__":
    unittest.main()
