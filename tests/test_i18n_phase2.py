import unittest
import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from i18n import I18n, i18n

class TestI18nPhase2(unittest.TestCase):
    def test_new_keys_exist(self):
        new_keys = [
            "version", "license", "update_available", "update_btn", 
            "env_info_title", "log_cli_start", "log_est_header", 
            "log_trial_est", "log_total_est", "log_start_bench_gui",
            "log_result_header", "log_error"
        ]
        for lang in ["ja", "en"]:
            obj = I18n(lang=lang)
            for key in new_keys:
                with self.subTest(lang=lang, key=key):
                    text = obj.t(key)
                    self.assertNotEqual(text, key, f"Key '{key}' not found in {lang}")

    def test_formatting(self):
        i18n.set_lang("ja")
        text = i18n.t("update_available", version="1.0.0")
        self.assertIn("1.0.0", text)
        
        text = i18n.t("log_total_est", trials=10, min=5, sec=30)
        self.assertIn("10", text)
        self.assertIn("5", text)
        self.assertIn("30", text)

if __name__ == "__main__":
    unittest.main()
