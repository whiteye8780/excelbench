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
            "lang_label": "Language / 言語",
            "finish_title": "診断完了",
            "finish_msg": "ベンチマークが完了しました。\n\nCold Start: {cold}s\nHot Avg: {hot}s\n\n結果を `logs/report.txt` に保存しました。",
            "log_cleanup": "既存のExcelプロセスをクリーンアップ中...",
            "log_gen_file": "{row}行のテストファイルを生成中...",
            "log_create_inst": "Excelインスタンスを起動中...",
            "log_start_bench": "{row}行、{trials}回の計測を開始します...",
            "log_trial": "試行 {current}/{total} を実行中 ({type})",
            "log_trial_end": "試行 {current} 完了: {time} 秒",
            "log_gen_done": "テストファイルの生成が完了しました。",
            "log_bench_done": "すべての計測が完了しました。",
            "version": "バージョン",
            "license": "ライセンス情報",
            "update_available": "新しいバージョン ({version}) が利用可能です。",
            "update_btn": "ダウンロードページへ",
            "terms_of_use": "利用規約",
            "privacy_policy": "プライバシーポリシー",
            "env_info_title": "=== 環境情報 ===",
            "log_cli_start": "ExcelBench Phase 2 実行中 (CLI)...",
            "log_est_header": "【実行時間推定】 10,000行の計測結果({time}s)に基づく推定値:",
            "log_trial_est": " - 1試行あたりの想定時間: 約 {time} 秒",
            "log_total_est": " - 全 {trials} 試行の総想定時間: 約 {min} 分 {sec} 秒",
            "log_start_bench_gui": "> ベンチマークを開始します ({row}行)...",
            "log_result_header": "--- {result_title} ---",
            "log_error": "[エラー] {msg}",
            "cancelling": "停止中...",
            "cancelled_msg": "キャンセルしました。",
            "finish_title": "診断完了"
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
            "lang_label": "Language",
            "finish_title": "Diagnostic Complete",
            "finish_msg": "Benchmark has completed.\n\nCold Start: {cold}s\nHot Avg: {hot}s\n\nResults saved to `logs/report.txt`.",
            "log_cleanup": "Cleaning up existing Excel processes...",
            "log_gen_file": "Generating test file with {row} rows...",
            "log_create_inst": "Launching Excel instance...",
            "log_start_bench": "Starting benchmark: {row} rows, {trials} trials...",
            "log_trial": "Running Trial {current}/{total} ({type})",
            "log_trial_end": "Trial {current} completed: {time} sec",
            "log_gen_done": "Test file generation complete.",
            "log_bench_done": "Benchmark process complete.",
            "version": "Version",
            "license": "License Information",
            "update_available": "New version ({version}) is available.",
            "update_btn": "Go to Download Page",
            "terms_of_use": "Terms of Use",
            "privacy_policy": "Privacy Policy",
            "env_info_title": "=== Environment Info ===",
            "log_cli_start": "ExcelBench Phase 2 Starting (CLI)...",
            "log_est_header": "[Execution Time Estimation] Based on 10,000 rows results ({time}s):",
            "log_trial_est": " - Estimated per trial: Approx. {time} sec",
            "log_total_est": " - Total estimated time ({trials} trials): Approx. {min} min {sec} sec",
            "log_start_bench_gui": "> Starting Benchmark ({row} rows)...",
            "log_result_header": "--- {result_title} ---",
            "log_error": "[ERROR] {msg}",
            "cancelling": "Stopping...",
            "cancelled_msg": "Cancelled.",
            "finish_title": "Diagnostic Complete"
        }
    }

    def __init__(self, lang=None):
        if lang:
            self.lang = lang
        else:
            self.lang = self._get_system_lang()

    def _get_system_lang(self):
        try:
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
