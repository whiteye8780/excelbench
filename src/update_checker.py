import requests
from version import VERSION
from i18n import i18n
from logger import logger

class UpdateChecker:
    """
    GitHub Pages上の stats.json を参照してアップデートを確認するクラス。
    """
    STATS_URL = "https://whiteye8780.github.io/excelbench/stats.json" # 仮のURL

    @staticmethod
    def check_for_updates():
        """
        最新バージョンを確認し、現在のバージョンより新しければそのバージョン番号を返します。
        アップデートがない、またはエラーが発生した場合は None を返します。
        """
        try:
            # タイムアウトを設定してリクエスト
            response = requests.get(UpdateChecker.STATS_URL, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            latest_version = data.get("version")
            if latest_version and UpdateChecker._is_newer(latest_version, VERSION):
                return latest_version
        except Exception as e:
            logger.error(f"Failed to check for updates: {e}")
        
        return None

    @staticmethod
    def _is_newer(latest, current):
        """
        バージョン文字列を比較します (簡易実装)。
        """
        try:
            return [int(x) for x in latest.split(".")] > [int(x) for x in current.split(".")]
        except:
            return latest > current
