import customtkinter as ctk
import threading
import queue
import time
import os
from i18n import i18n
from benchmark import ExcelBenchmark, ExcelNotInstalledError
from logger import logger, report_logger
import system_info

class ExcelBenchGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title(i18n.t("title"))
        self.geometry("800x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # State
        self.benchmark_running = False
        self.log_queue = queue.Queue()
        self.bench = ExcelBenchmark()
        self.sys_info = {}
        self.excel_info = {}

        self._build_ui()
        self._load_info()
        self._check_logs()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Header & Language Switcher
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(header_frame, text=i18n.t("title"), font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, sticky="w")

        self.lang_var = ctk.StringVar(value=i18n.lang)
        lang_switch = ctk.CTkOptionMenu(
            header_frame, values=["ja", "en"], variable=self.lang_var, command=self._change_lang, width=80
        )
        lang_switch.grid(row=0, column=1, sticky="e")

        # 2. System Info Card
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        info_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.cpu_label = ctk.CTkLabel(info_frame, text=f"{i18n.t('cpu')}: ---", font=ctk.CTkFont(size=12))
        self.cpu_label.grid(row=0, column=0, padx=10, pady=10)

        self.mem_label = ctk.CTkLabel(info_frame, text=f"{i18n.t('memory')}: ---", font=ctk.CTkFont(size=12))
        self.mem_label.grid(row=0, column=1, padx=10, pady=10)

        self.storage_label = ctk.CTkLabel(info_frame, text=f"{i18n.t('storage')}: ---", font=ctk.CTkFont(size=12))
        self.storage_label.grid(row=0, column=2, padx=10, pady=10)

        self.excel_label = ctk.CTkLabel(info_frame, text=f"{i18n.t('excel_ver')}: --- (---)", font=ctk.CTkFont(size=12))
        self.excel_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10))

        # 3. Settings & Controls
        control_frame = ctk.CTkFrame(self)
        control_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        control_frame.grid_columnconfigure(0, weight=1)

        settings_label = ctk.CTkLabel(control_frame, text=i18n.t("settings_title"), font=ctk.CTkFont(size=16, weight="bold"))
        settings_label.grid(row=0, column=0, pady=(15, 5))

        self.row_var = ctk.IntVar(value=10000)
        row_choice = ctk.CTkSegmentedButton(
            control_frame, values=["10000", "50000", "100000"],
            command=self._on_row_change
        )
        row_choice.set("10000")
        row_choice.grid(row=1, column=0, padx=20, pady=10)

        # Warning/Estimation Area
        self.warning_label = ctk.CTkLabel(control_frame, text="", text_color="#FFCC00")
        self.warning_label.grid(row=2, column=0, pady=5)

        self.run_button = ctk.CTkButton(
            control_frame, text=i18n.t("run_bench"), height=50,
            command=self._toggle_benchmark, font=ctk.CTkFont(size=16, weight="bold")
        )
        self.run_button.grid(row=3, column=0, padx=40, pady=20, sticky="ew")

        # 4. Progress & Log
        self.progress_bar = ctk.CTkProgressBar(control_frame)
        self.progress_bar.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.progress_bar.set(0)

        self.log_textbox = ctk.CTkTextbox(control_frame, height=200)
        self.log_textbox.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="nsew")
        control_frame.grid_rowconfigure(5, weight=1)

    def _load_info(self):
        """システム情報をバックグラウンドで読み込みます。"""
        def load():
            try:
                self.sys_info = system_info.get_all_system_info()
                self.excel_info = self.bench.get_excel_info()
                self.after(0, self._update_info_display)
            except Exception as e:
                logger.error(f"Failed to load info: {e}")

        threading.Thread(target=load, daemon=True).start()

    def _update_info_display(self):
        self.cpu_label.configure(text=f"{i18n.t('cpu')}: {self.sys_info.get('CPU', 'Unknown')}")
        self.mem_label.configure(text=f"{i18n.t('memory')}: {self.sys_info.get('Memory', 'Unknown')}")
        self.storage_label.configure(text=f"{i18n.t('storage')}: {self.sys_info.get('Storage', 'Unknown')}")
        
        ver = self.excel_info.get('Version', 'Unknown')
        arch = self.excel_info.get('Architecture', 'Unknown')
        self.excel_label.configure(text=f"{i18n.t('excel_ver')}: {ver} ({arch})")

        # 初期レポート出力
        report_logger.info("=== Environment Info (GUI) ===")
        report_logger.info(f"CPU: {self.sys_info.get('CPU')}")
        report_logger.info(f"Memory: {self.sys_info.get('Memory')}")
        report_logger.info(f"Storage: {self.sys_info.get('Storage')}")
        report_logger.info(f"Excel: {ver} ({arch})")
        report_logger.info("========================")

    def _on_row_change(self, value):
        rows = int(value)
        self.row_var.set(rows)
        if rows >= 100000:
            self.warning_label.configure(text=i18n.t("warning_100k"))
        else:
            self.warning_label.configure(text="")

    def _change_lang(self, lang):
        i18n.set_lang(lang)
        self.destroy()
        ExcelBenchGUI().mainloop()

    def _toggle_benchmark(self):
        if self.benchmark_running:
            return # TODO: 停止処理の検討
        
        self.benchmark_running = True
        self.run_button.configure(state="disabled", text="Running...")
        self.log_textbox.delete("1.0", "end")
        self.progress_bar.set(0)
        
        row_count = self.row_var.get()
        threading.Thread(target=self._run_benchmark_thread, args=(row_count,), daemon=True).start()

    def _run_benchmark_thread(self, row_count):
        trials = 10
        try:
            # 1. Estimation if 100k
            if row_count >= 100000:
                self.log_queue.put(f"> {i18n.t('estimating')}")
                probe = self.bench.run_benchmark(row_count=10000, trials=1)
                p_time = probe['cold_start']
                est_time = p_time * (10**1.86) * trials
                m, s = divmod(int(est_time), 60)
                msg = i18n.t("estimated_time", min=m, sec=s)
                self.log_queue.put(f"> {msg}")
                self.after(0, lambda: self.warning_label.configure(text=msg))

            # 2. Main Benchmark
            self.log_queue.put(f"> Starting Benchmark ({row_count} rows)...")
            
            # カスタムロガーの出力をキューに流すための工夫が必要だが、
            # ここでは進捗状況を個別にputする
            
            results = self.bench.run_benchmark(row_count=row_count, trials=trials)
            
            self.log_queue.put("--- Result ---")
            self.log_queue.put(f"Cold Start: {results['cold_start']:.4f}s")
            self.log_queue.put(f"Hot Avg: {results['average_hot']:.4f}s")
            
            report_logger.info(f"GUI Result - Rows: {row_count}, Cold: {results['cold_start']:.4f}, HotAvg: {results['average_hot']:.4f}")

        except ExcelNotInstalledError:
            self.log_queue.put(f"[ERROR] {i18n.t('excel_not_found')}")
        except Exception as e:
            self.log_queue.put(f"[ERROR] {str(e)}")
        finally:
            self.benchmark_running = False
            self.after(0, lambda: self.run_button.configure(state="normal", text=i18n.t("run_bench")))

    def _check_logs(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_textbox.insert("end", msg + "\n")
                self.log_textbox.see("end")
        except queue.Empty:
            pass
        self.after(100, self._check_logs)

if __name__ == "__main__":
    app = ExcelBenchGUI()
    app.mainloop()
