import os
import time
import random
from datetime import datetime
from logger import logger
from i18n import i18n

class ExcelNotInstalledError(Exception):
    """Excelがインストールされていない、または自動操作が不可能な場合に投げられる例外。"""
    pass

class ExcelBenchmark:
    """
    Excelの起動、ファイル生成、再計算計測を行うクラス。
    """
    OFFICE_DOWNLOAD_URL = "https://www.microsoft.com/ja-jp/microsoft-365/buy/microsoft-365"

    def __init__(self, data_dir="data"):
        self.data_dir = os.path.join(os.getcwd(), data_dir)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.excel = None

    def cleanup_processes(self):
        """
        既存のExcelプロセスをクリーンアップします。
        (実際には慎重に行う必要がありますが、ベンチマーク環境を整えるために必要です)
        """
        try:
            os.system('taskkill /f /im excel.exe >nul 2>&1')
            logger.info(i18n.t("log_cleanup"))
            self.excel = None  # プロセスを落としたので、インスタンス参照をクリアする
            time.sleep(1)
        except Exception as e:
            logger.error(f"Failed to cleanup Excel processes: {e}")

    def create_instance(self):
        """
        新しいExcelインスタンスを生成します。
        Excelがインストールされていない場合は ExcelNotInstalledError を投げます。
        """
        try:
            import win32com.client
            # DispatchExを使用して新しいインスタンスを確実に生成する
            self.excel = win32com.client.DispatchEx("Excel.Application")
            self.excel.Visible = False
            self.excel.DisplayAlerts = False
            logger.info(i18n.t("log_create_inst"))
            return self.excel
        except Exception as e:
            # クラス名やエラーメッセージから未インストールを判断
            error_msg = str(e)
            if "Invalid class string" in error_msg or "failed" in error_msg.lower():
                logger.error(f"Excel is not installed or not found: {e}")
                raise ExcelNotInstalledError("Microsoft Excel が見つかりません。")
            logger.error(f"Failed to create Excel instance: {e}")
            raise

    def get_excel_info(self):
        """
        インストールされているExcelのバージョンとアーキテクチャ(32bit/64bit)を取得します。
        """
        temp_excel = None
        try:
            import win32com.client
            temp_excel = win32com.client.Dispatch("Excel.Application")
            version = temp_excel.Version
            
            # アーキテクチャの判別
            is_64bit = "64-bit" if "64" in temp_excel.OperatingSystem else "32-bit"

            return {
                "Version": version,
                "Architecture": is_64bit
            }
        except Exception as e:
            logger.error(f"Failed to get Excel info: {e}")
            return {"Version": "Unknown", "Architecture": "Unknown"}
        finally:
            if temp_excel:
                try:
                    temp_excel.Quit()
                except:
                    pass

    def generate_test_file(self, row_count=10000):
        """
        ベンチマーク用のファイルを生成します。
        A列: RANDBETWEEN
        B列: 連番
        C列: COUNTIF
        """
        file_path = os.path.join(self.data_dir, f"bench_{row_count}_{int(time.time())}.xlsx")
        logger.info(i18n.t("log_gen_file", row=row_count))
        
        try:
            if not self.excel:
                self.create_instance()

            wb = self.excel.Workbooks.Add()
            ws = wb.ActiveSheet

            # 大量データ入力の高速化のために配列を使用（今回は簡易的に数式を指定）
            # A列: =RANDBETWEEN(1, 10000)
            ws.Range(f"A1:A{row_count}").Formula = "=RANDBETWEEN(1, 10000)"
            # B列: 連番
            ws.Range(f"B1:B{row_count}").Formula = "=ROW()"
            # C列: =COUNTIF($A$1:$A$10000, A1)
            ws.Range(f"C1:C{row_count}").Formula = f"=COUNTIF($A$1:$A${row_count}, A1)"

            wb.SaveAs(file_path)
            wb.Close()
            logger.info(i18n.t("log_gen_done"))
            return file_path
        except Exception as e:
            logger.error(f"Error generating test file: {e}")
            if 'wb' in locals(): wb.Close(False)
            raise

    def measure_open_time(self, file_path):
        """
        ファイルのオープンから計算完了までの時間を計測します。
        """
        start_time = time.perf_counter()
        try:
            wb = self.excel.Workbooks.Open(file_path)
            # 全計算完了を待機
            self.excel.CalculateUntilAsyncQueriesDone()
            end_time = time.perf_counter()
            wb.Close(False)
            duration = end_time - start_time
            return duration
        except Exception as e:
            logger.error(f"Error during measurement: {e}")
            raise

    def run_benchmark(self, row_count=10000, trials=10, progress_callback=None):
        """
        ベンチマークプロトコルを実行します。
        progress_callback: (current_trial, total_trials) を引数に取る関数
        """
        logger.info(i18n.t("log_start_bench", row=row_count, trials=trials))
        results = []
        
        try:
            # 1. クリーンアップ
            self.cleanup_processes()
            
            # 2. ファイル生成
            file_path = self.generate_test_file(row_count)
            
            # 3. 計測開始
            self.create_instance()
            
            for i in range(trials):
                trial_type_label = i18n.t("cold_start") if i == 0 else i18n.t("hot_start")
                logger.info(i18n.t("log_trial", current=i+1, total=trials, type=trial_type_label))
                
                duration = self.measure_open_time(file_path)
                results.append(duration)
                
                logger.info(i18n.t("log_trial_end", current=i+1, time=f"{duration:.4f}"))
                
                if progress_callback:
                    progress_callback(i + 1, trials)
                    
                time.sleep(0.5) # インターバル

            self.excel.Quit()
            self.excel = None
            
            logger.info(i18n.t("log_bench_done"))
            
            return {
                "row_count": row_count,
                "cold_start": results[0],
                "hot_starts": results[1:],
                "average_hot": sum(results[1:]) / len(results[1:]) if len(results) > 1 else 0
            }

        except Exception as e:
            logger.error(f"Benchmark failed: {e}")
            if self.excel:
                try: self.excel.Quit()
                except: pass
            raise
        finally:
            # テンプファイルを削除するかは要件次第だが、基本は残して後で消す
            pass

if __name__ == "__main__":
    bench = ExcelBenchmark()
    # 簡易実行テスト
    try:
        res = bench.run_benchmark(row_count=1000, trials=3)
        logger.info(res)
    except Exception as e:
        logger.error(f"Benchmark test failed: {e}")
