import platform
import psutil
import socket
import os
import subprocess
from logger import logger

def get_cpu_info():
    """CPU名を取得します。"""
    try:
        if platform.system() == "Windows":
            return platform.processor()
        return platform.machine()
    except Exception as e:
        logger.error(f"Failed to get CPU info: {e}")
        return "Unknown CPU"

def get_memory_info():
    """総メモリ容量をGB単位で取得します。"""
    try:
        total_memory = psutil.virtual_memory().total
        return f"{total_memory / (1024 ** 3):.1f} GB"
    except Exception as e:
        logger.error(f"Failed to get memory info: {e}")
        return "Unknown Memory"

def get_storage_type():
    """
    実行ドライブのストレージ種類（SSD/HDD）を判別します。
    Windows環境でPowerShellを使用して判定します。
    """
    try:
        drive = os.path.splitdrive(os.getcwd())[0] if os.path.splitdrive(os.getcwd())[0] else "C:"
        # PowerShellを使用してメディアタイプを判定
        cmd = f'Get-PhysicalDisk | Where-Object {{ $_.DeviceID -eq (Get-Partition -DriveLetter {drive.strip(":")} | Get-Disk).Number }} | Select-Object -ExpandProperty MediaType'
        # 出力をより安全にパースする
        process = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True)
        result = process.stdout.strip()
        
        if not result:
            return "Unknown Storage (Empty result)"
        return result
    except Exception as e:
        logger.error(f"Failed to detect storage type: {e}")
        return "Unknown Storage (Detect Failed)"

def get_all_system_info():
    """すべてのシステム情報を辞書で返します。"""
    return {
        "CPU": get_cpu_info(),
        "Memory": get_memory_info(),
        "Storage": get_storage_type()
    }
