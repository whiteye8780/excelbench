import locale
import ctypes

class I18n:
    TRANSLATIONS = {
        "ja": {
            "title": "ExcelBench - PC業務適正診断",
            "sys_info_title": "システム情報",
            "cpu": "CPU",
            "memory": "メモリ",
            "storage": "ストレージ",
            "excel_ver": "Excelバージョン",
            "excel_arch": "Excelアーキテクチャ",
            "settings_title": "計測設定",
            "row_count": "計測行数",
            "run_bench": "ベンチマーク開始",
            "stop_bench": "停止",
            "log_title": "進捗ログ",
            "result_title": "計測結果",
            "cold_start": "Cold Start (初回)",
            "hot_start": "Hot Start (平均)",
            "warning_100k": "100,000行が選択されました。動作が非常に重くなる可能性があります。",
            "estimating": "実行時間を推定中...",
            "estimated_time": "想定実行時間: 約 {min} 分 {sec} 秒",
            "excel_not_found": "Excelが見つかりません。インストールが必要です。",
            "lang_label": "Language / 言語"
        },
        "en": {
            "title": "ExcelBench - PC Business Suitability Diagnostic",
            "sys_info_title": "System Information",
            "cpu": "CPU",
            "memory": "Memory",
            "storage": "Storage",
            "excel_ver": "Excel Version",
            "excel_arch": "Excel Architecture",
            "settings_title": "Benchmark Settings",
            "row_count": "Row Count",
            "run_bench": "Start Benchmark",
            "stop_bench": "Stop",
            "log_title": "Progress Log",
            "result_title": "Results",
            "cold_start": "Cold Start",
            "hot_start": "Hot Start (Avg)",
            "warning_100k": "100,000 rows selected. Performance may be significantly impacted.",
            "estimating": "Estimating execution time...",
            "estimated_time": "Estimated Time: ~ {min} min {sec} sec",
            "excel_not_found": "Excel not found. Installation required.",
            "lang_label": "Language"
        }
    }

    def __init__(self, lang=None):
        if lang:
            self.lang = lang
        else:
            self.lang = self._get_system_lang()

    def _get_system_lang(self):
        try:
            # WindowsのUI言語を取得
            windll = ctypes.windll.kernel32
            lang_id = windll.GetUserDefaultUILanguage()
            primary_lang = locale.windows_locale.get(lang_id, "en_US")
            if "ja" in primary_lang.lower():
                return "ja"
        except:
            pass
        return "en"

    def t(self, key, **kwargs):
        text = self.TRANSLATIONS.get(self.lang, self.TRANSLATIONS["en"]).get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text

    def set_lang(self, lang):
        if lang in self.TRANSLATIONS:
            self.lang = lang

# Singleton instance
i18n = I18n()
