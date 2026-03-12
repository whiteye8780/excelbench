import os
import sys

def get_base_dir():
    """
    アプリケーションのベースディレクトリを取得します。
    開発時（python実行）はプロジェクトルート。
    本番時（EXE実行）はユーザーのドキュメントフォルダ内。
    """
    # PyInstallerで実行されているか判定
    is_frozen = getattr(sys, 'frozen', False)
    
    if is_frozen:
        # 本番環境: Document\ExcelBench
        base = os.path.join(os.path.expanduser("~"), "Documents", "ExcelBench")
    else:
        # 開発環境: プロジェクトルート (srcの親ディレクトリ)
        # __file__ を基準にする
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    if not os.path.exists(base):
        os.makedirs(base, exist_ok=True)
    return base

def get_log_dir():
    log_dir = os.path.join(get_base_dir(), "logs")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir

def get_data_dir():
    data_dir = os.path.join(get_base_dir(), "data")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir
