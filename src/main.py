import argparse
import sys
import os
from logger import logger, report_logger
from benchmark import ExcelBenchmark, ExcelNotInstalledError
import system_info

def cli_main(args):
    try:
        row_count = args.rows
        trials = args.trials

        logger.info("ExcelBench Phase 1 Prototype Starting (CLI)...")
        
        # システム情報とExcel情報の取得・表示
        sys_info = system_info.get_all_system_info()
        logger.info(f"System Info: {sys_info}")
        
        bench = ExcelBenchmark()
        excel_info = bench.get_excel_info()
        logger.info(f"Excel Info: {excel_info}")

        # レポートへの記録
        report_logger.info("=== Environment Info (CLI) ===")
        report_logger.info(f"CPU: {sys_info['CPU']}")
        report_logger.info(f"Memory: {sys_info['Memory']}")
        report_logger.info(f"Storage: {sys_info['Storage']}")
        report_logger.info(f"Excel Version: {excel_info['Version']}")
        report_logger.info(f"Excel Arch: {excel_info['Architecture']}")
        report_logger.info("========================")

        if row_count >= 100000:
            logger.info("100,000行の実行時間を推定するため、10,000行での試行計測を開始します...")
            probe_stats = bench.run_benchmark(row_count=10000, trials=1)
            probe_time = probe_stats['cold_start']
            
            estimated_trial_time = probe_time * (10**1.86)
            estimated_total_time = estimated_trial_time * trials
            
            est_min = int(estimated_total_time // 60)
            est_sec = int(estimated_total_time % 60)
            
            logger.info(f"【実行時間推定】 10,000行の計測結果({probe_time:.2f}s)に基づく推定値:")
            logger.info(f"  - 1試行あたりの想定時間: 約 {estimated_trial_time:.1f} 秒")
            logger.info(f"  - 全 {trials} 試行の総想定時間: 約 {est_min} 分 {est_sec} 秒")
            report_logger.info(f"[推定実行時間] 総計約 {est_min}分 {est_sec}秒 (10k baseline: {probe_time:.2f}s)")
            logger.info("本番の100,000行ベンチマークを開始します...")

        logger.info(f"Row Count: {row_count}, Trials: {trials}")
        stats = bench.run_benchmark(row_count=row_count, trials=trials)
        
        # ユーザーレポート用出力
        report_logger.info("--- ExcelBench Benchmark Execution ---")
        report_logger.info(f"Row Count: {row_count}")
        report_logger.info(f"Cold Start: {stats['cold_start']:.4f} sec")
        report_logger.info(f"Hot Start Average: {stats['average_hot']:.4f} sec")
        report_logger.info("--------------------------------------")

        logger.info("--- Benchmark Results ---")
        logger.info(f"Cold Start: {stats['cold_start']:.4f} sec")
        logger.info(f"Hot Start Average: {stats['average_hot']:.4f} sec")

    except ExcelNotInstalledError as e:
        logger.error(f"Excel Check Failed: {e}")
        report_logger.error(f"[エラー] {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
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
