import PyInstaller.__main__
import os
import shutil

def build():
    # 出力先ディレクトリの整理
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")

    # PyInstallerのオプション設定
    opts = [
        'src/main.py',              # メインスクリプト
        '--name=ExcelBench',        # 生成されるEXEの名前
        '--onefile',                # 1つのファイルにまとめる
        '--noconsole',              # コンソールを表示しない
        '--collect-all=customtkinter', 
        '--add-data=docs;docs',     # ドキュメントを同梱
        '--add-data=src/i18n.py;.', # 個別インポートが必要なものを手動追加検討
        '--clean'
    ]

    # 追加データのリソースパスをビルドスクリプト側で動的に指定する場合
    # (src全体を含めるとサイズが大きくなるため、実行に必要なものに絞る)
    
    # 実際には --collect-submodules 等も検討可能


    print(f"Starting build with options: {' '.join(opts)}")
    PyInstaller.__main__.run(opts)
    print("Build complete. Output in dist/ExcelBench.exe")

if __name__ == "__main__":
    build()
    # ビルド後にZIPを作成
    try:
        from create_zip import create_dist_zip
        create_dist_zip()
    except Exception as e:
        print(f"Error during ZIP creation: {e}")
