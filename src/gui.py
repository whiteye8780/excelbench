import customtkinter as ctk
import threading
import queue
import pythoncom
import time
import os
from i18n import i18n
from benchmark import ExcelBenchmark, ExcelNotInstalledError
from logger import logger, report_logger
import system_info
import logging
from tkinter import messagebox

class GUILogHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        log_entry = self.format(record)
        self.log_queue.put(log_entry)

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

        # Logging redirection
        self._setup_logging()

        self._build_ui()
        self._load_info()
        self._check_logs()
        self._check_updates()

    def _setup_logging(self):
        handler = GUILogHandler(self.log_queue)
        formatter = logging.Formatter('%(message)s') # シンプルにする
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logging.getLogger("excelbench").addHandler(handler)

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
        self.log_textbox.grid(row=5, column=0, padx=20, pady=(10, 10), sticky="nsew")
        control_frame.grid_rowconfigure(5, weight=1)

        # 5. Footer (Version & Licenses)
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        from version import VERSION
        self.ver_label = ctk.CTkLabel(footer_frame, text=f"v{VERSION}", font=ctk.CTkFont(size=10))
        self.ver_label.pack(side="left", padx=10)

        self.license_btn = ctk.CTkButton(
            footer_frame, text=i18n.t("license"), width=100, height=20,
            fg_color="gray", hover_color="#555555",
            font=ctk.CTkFont(size=10), command=self._show_licenses
        )
        self.license_btn.pack(side="right", padx=10)

        # Update Notification Area (Hidden by default)
        self.update_frame = ctk.CTkFrame(self, fg_color="#2B2B2B", height=0)
        self.update_label = ctk.CTkLabel(self.update_frame, text="", font=ctk.CTkFont(size=12))
        self.update_btn = ctk.CTkButton(self.update_frame, text=i18n.t("update_btn"), height=25, command=self._open_download_page)
        
        # 6. Legal Links in Footer
        legal_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        legal_frame.pack(side="right", padx=10)

        self.privacy_btn = ctk.CTkButton(
            legal_frame, text=i18n.t("privacy_policy"), width=100, height=20,
            fg_color="transparent", text_color="gray", hover_color="#333333",
            font=ctk.CTkFont(size=9, underline=True), command=self._show_privacy
        )
        self.privacy_btn.pack(side="right", padx=5)

        self.terms_btn = ctk.CTkButton(
            legal_frame, text=i18n.t("terms_of_use"), width=80, height=20,
            fg_color="transparent", text_color="gray", hover_color="#333333",
            font=ctk.CTkFont(size=9, underline=True), command=self._show_terms
        )
        self.terms_btn.pack(side="right", padx=5)
        
    def _show_licenses(self):
        from licenses import LICENSE_TEXT
        license_win = ctk.CTkToplevel(self)
        license_win.title(i18n.t("license"))
        license_win.geometry("600x400")
        license_win.attributes("-topmost", True)
        
        txt = ctk.CTkTextbox(license_win)
        txt.pack(fill="both", expand=True, padx=20, pady=20)
        txt.insert("1.0", LICENSE_TEXT)
        txt.configure(state="disabled")

    def _open_download_page(self):
        import webbrowser
        webbrowser.open(self.bench.OFFICE_DOWNLOAD_URL) # 現状は暫定

    def _show_terms(self):
        self._open_local_doc("terms.md")

    def _show_privacy(self):
        self._open_local_doc("privacy.md")

    def _open_local_doc(self, filename):
        import webbrowser
        # ビルド後と開発環境の両方に対応するように paths モジュールでも考慮しているが、 
        # ここでは docs フォルダ（リソース）を参照するので従来のパス解決を維持
        base_path = os.path.dirname(os.path.abspath(__file__))
        doc_path = os.path.join(base_path, "..", "docs", filename)
        if not os.path.exists(doc_path):
            # PyInstaller内部のパス (_MEIPASS) を考慮
            if hasattr(sys, '_MEIPASS'):
                doc_path = os.path.join(sys._MEIPASS, "docs", filename)
        
        if os.path.exists(doc_path):
            webbrowser.open(f"file:///{os.path.abspath(doc_path)}")
        else:
            messagebox.showerror("Error", f"Document not found: {filename}")

    def _check_updates(self):
        """アップデートを確認します。"""
        def check():
            from update_checker import UpdateChecker
            latest_ver = UpdateChecker.check_for_updates()
            if latest_ver:
                self.after(0, lambda: self._show_update_notice(latest_ver))
        
        threading.Thread(target=check, daemon=True).start()

    def _show_update_notice(self, version):
        self.update_frame.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.update_label.configure(text=i18n.t("update_available", version=version))
        self.update_label.pack(side="left", padx=10, pady=5)
        self.update_btn.pack(side="right", padx=10, pady=5)

    def _load_info(self):
        """システム情報をバックグラウンドで読み込みます。"""
        def load():
            pythoncom.CoInitialize()
            try:
                self.sys_info = system_info.get_all_system_info()
                self.excel_info = self.bench.get_excel_info()
                self.after(0, self._update_info_display)
            except Exception as e:
                logger.error(f"Failed to load info: {e}")
            finally:
                pythoncom.CoUninitialize()

        threading.Thread(target=load, daemon=True).start()

    def _update_info_display(self):
        self.cpu_label.configure(text=f"{i18n.t('cpu')}: {self.sys_info.get('CPU', 'Unknown')}")
        self.mem_label.configure(text=f"{i18n.t('memory')}: {self.sys_info.get('Memory', 'Unknown')}")
        self.storage_label.configure(text=f"{i18n.t('storage')}: {self.sys_info.get('Storage', 'Unknown')}")
        
        ver = self.excel_info.get('Version', 'Unknown')
        arch = self.excel_info.get('Architecture', 'Unknown')
        self.excel_label.configure(text=f"{i18n.t('excel_ver')}: {ver} ({arch})")

        # 初期レポート出力
        report_logger.info(i18n.t("env_info_title"))
        report_logger.info(f"CPU: {self.sys_info.get('CPU')}")
        report_logger.info(f"Memory: {self.sys_info.get('Memory')}")
        report_logger.info(f"Storage: {self.sys_info.get('Storage')}")
        report_logger.info(f"Excel: {ver} ({arch})")
        report_logger.info("=" * 24)

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
            self.bench.is_cancelled = True
            self.run_button.configure(state="disabled", text=i18n.t("cancelling"))
            return
        
        self.benchmark_running = True
        self.bench.is_cancelled = False
        self.run_button.configure(text=i18n.t("stop_bench"))
        self.log_textbox.delete("1.0", "end")
        self.progress_bar.set(0)
        
        row_count = self.row_var.get()
        threading.Thread(target=self._run_benchmark_thread, args=(row_count,), daemon=True).start()

    def _run_benchmark_thread(self, row_count):
        pythoncom.CoInitialize()
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
            self.log_queue.put(i18n.t("log_start_bench_gui", row=row_count))
            
            def progress_callback(current, total):
                progress = current / total
                self.after(0, lambda: self.progress_bar.set(progress))

            results = self.bench.run_benchmark(
                row_count=row_count, 
                trials=trials, 
                progress_callback=progress_callback
            )
            
            if results is None or self.bench.is_cancelled:
                self.log_queue.put(i18n.t("cancelled_msg"))
                self.after(0, lambda: messagebox.showinfo(
                    i18n.t("finish_title"),
                    i18n.t("cancelled_msg")
                ))
                return

            self.log_queue.put(i18n.t("log_result_header", result_title=i18n.t('result_title')))
            self.log_queue.put(f"{i18n.t('cold_start')}: {results['cold_start']:.4f}s")
            self.log_queue.put(f"{i18n.t('hot_start')}: {results['average_hot']:.4f}s")
            
            # Show Completion Massagebox
            self.after(0, lambda: messagebox.showinfo(
                i18n.t("finish_title"),
                i18n.t("finish_msg", cold=f"{results['cold_start']:.4f}", hot=f"{results['average_hot']:.4f}")
            ))
            
            report_logger.info(f"GUI Result - Rows: {row_count}, Cold: {results['cold_start']:.4f}, HotAvg: {results['average_hot']:.4f}")

        except ExcelNotInstalledError:
            self.log_queue.put(i18n.t("log_error", msg=i18n.t('excel_not_found')))
        except Exception as e:
            self.log_queue.put(i18n.t("log_error", msg=str(e)))
        finally:
            self.benchmark_running = False
            self.after(0, lambda: self.run_button.configure(state="normal", text=i18n.t("run_bench")))
            pythoncom.CoUninitialize()

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
