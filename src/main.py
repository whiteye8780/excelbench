import argparse
import sys
import os
from logger import logger, report_logger
from benchmark import ExcelBenchmark, ExcelNotInstalledError
from i18n import i18n
import system_info

def cli_main(args):
    try:
        row_count = args.rows
        trials = args.trials

        logger.info(i18n.t("log_cli_start"))
        
        # システム情報とExcel情報の取得・表示
        sys_info = system_info.get_all_system_info()
        logger.info(f"{i18n.t('sys_info_title')}: {sys_info}")
        
        bench = ExcelBenchmark()
        excel_info = bench.get_excel_info()
        logger.info(f"{i18n.t('excel_ver')}: {excel_info}")

        # レポートへの記録
        report_logger.info(i18n.t("env_info_title"))
        report_logger.info(f"{i18n.t('cpu')}: {sys_info['CPU']}")
        report_logger.info(f"{i18n.t('memory')}: {sys_info['Memory']}")
        report_logger.info(f"{i18n.t('storage')}: {sys_info['Storage']}")
        report_logger.info(f"{i18n.t('excel_ver')}: {excel_info['Version']}")
        report_logger.info(f"{i18n.t('excel_arch')}: {excel_info['Architecture']}")
        report_logger.info("=" * 24)

        if row_count >= 100000:
            logger.info(i18n.t("estimating"))
            probe_stats = bench.run_benchmark(row_count=10000, trials=1)
            probe_time = probe_stats['cold_start']
            
            estimated_trial_time = probe_time * (10**1.86)
            estimated_total_time = estimated_trial_time * trials
            
            est_min = int(estimated_total_time // 60)
            est_sec = int(estimated_total_time % 60)
            
            logger.info(i18n.t("log_est_header", time=f"{probe_time:.2f}"))
            logger.info(i18n.t("log_trial_est", time=f"{estimated_trial_time:.1f}"))
            logger.info(i18n.t("log_total_est", trials=trials, min=est_min, sec=est_sec))
            
            report_logger.info(f"[{i18n.t('estimating')}] {est_min}m {est_sec}s (10k baseline: {probe_time:.2f}s)")
            logger.info("-" * 10)

        logger.info(f"{i18n.t('row_count')}: {row_count}, Trials: {trials}")
        stats = bench.run_benchmark(row_count=row_count, trials=trials)
        
        # ユーザーレポート用出力
        report_logger.info(i18n.t("log_result_header", result_title=i18n.t('result_title')))
        report_logger.info(f"{i18n.t('row_count')}: {row_count}")
        report_logger.info(f"{i18n.t('cold_start')}: {stats['cold_start']:.4f} sec")
        report_logger.info(f"{i18n.t('hot_start')}: {stats['average_hot']:.4f} sec")
        report_logger.info("-" * 38)

        logger.info(i18n.t("log_result_header", result_title=i18n.t('result_title')))
        logger.info(f"{i18n.t('cold_start')}: {stats['cold_start']:.4f} sec")
        logger.info(f"{i18n.t('hot_start')}: {stats['average_hot']:.4f} sec")

    except ExcelNotInstalledError as e:
        logger.error(i18n.t("log_error", msg=f"Excel Check Failed: {e}"))
        report_logger.error(i18n.t("log_error", msg=str(e)))
        sys.exit(1)
    except Exception as e:
        logger.error(i18n.t("log_error", msg=f"An unexpected error occurred: {e}"), exc_info=True)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="ExcelBench - PC Business Suitability Diagnostic")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--rows", type=int, default=10000, help="Number of rows for benchmark (CLI only)")
    parser.add_argument("--trials", type=int, default=10, help="Number of trials (CLI only)")
    args = parser.parse_args()

    if args.cli:
        cli_main(args)
    else:
        try:
            from gui import ExcelBenchGUI
            app = ExcelBenchGUI()
            app.mainloop()
        except ImportError:
            logger.error("GUI dependencies missing. Falling back to CLI.")
            cli_main(args)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()
