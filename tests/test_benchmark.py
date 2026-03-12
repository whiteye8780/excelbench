import unittest
import os
import sys
import shutil

# srcディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from benchmark import ExcelBenchmark

class TestExcelBenchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data_dir = "test_data"
        cls.bench = ExcelBenchmark(data_dir=cls.test_data_dir)

    @classmethod
    def tearDownClass(cls):
        # テストデータの削除
        if os.path.exists(cls.test_data_dir):
            shutil.rmtree(cls.test_data_dir)

    def test_directory_creation(self):
        self.assertTrue(os.path.exists(self.bench.data_dir))

    def test_excel_instance_creation(self):
        try:
            excel = self.bench.create_instance()
            self.assertIsNotNone(excel)
            excel.Quit()
        except Exception as e:
            self.fail(f"Excel instance creation failed: {e}")

    def test_file_generation(self):
        try:
            row_count = 100
            file_path = self.bench.generate_test_file(row_count=row_count)
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(file_path.endswith(".xlsx"))
        except Exception as e:
            self.fail(f"File generation failed: {e}")

if __name__ == "__main__":
    unittest.main()
