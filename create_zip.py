import zipfile
import os
from src.version import VERSION

def create_dist_zip():
    zip_name = f"ExcelBench_v{VERSION}.zip"
    dist_dir = "dist"
    exe_file = "ExcelBench.exe"
    exe_path = os.path.join(dist_dir, exe_file)

    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found. Please run build.py first.")
        return

    print(f"Creating {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        #EXEの追加
        zipf.write(exe_path, exe_file)
        
        # docs内のMarkdownを同梱（ビルド済みEXEの中にもあるが、外からも見れるように）
        docs_dir = "docs"
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith((".md", ".txt", ".json")):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.join("docs", file))

    print(f"Successfully created {zip_name}")

if __name__ == "__main__":
    create_dist_zip()
