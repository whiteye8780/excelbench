import logging
import os
from datetime import datetime
from paths import get_log_dir

def setup_logger(name="excelbench"):
    """
    システムの共通ロガーをセットアップします。
    logsフォルダに日付別のログファイルを作成し、コンソールにも出力します。
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # すでにハンドラが設定されている場合は重複を避ける
    if logger.handlers:
        return logger

    # ログフォルダの指定
    log_dir = get_log_dir()

    # フォーマット設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # ファイル出力設定 (日付別)
    log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(
        os.path.join(log_dir, log_filename), 
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # コンソール出力設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def setup_report_logger(name="excelbench_report"):
    """
    ユーザー向けの実行結果を記録するロガーをセットアップします。
    logs/report.txt に実行結果を追記します。
    """
    report_logger = logging.getLogger(name)
    report_logger.setLevel(logging.INFO)

    if report_logger.handlers:
        return report_logger

    log_dir = get_log_dir()

    # ユーザー向けレポートはシンプルな形式にする
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    report_file = os.path.join(log_dir, "report.txt")
    file_handler = logging.FileHandler(report_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    report_logger.addHandler(file_handler)
    return report_logger

# デフォルトロガーのインスタンスを提供
logger = setup_logger()
report_logger = setup_report_logger()
