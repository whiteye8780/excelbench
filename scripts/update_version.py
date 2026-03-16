import os
import re

def update_html_version(content: str, new_version: str) -> str:
    """
    HTMLコンテンツ内のバージョン表記を置換する関数
    例: <span class="version-tag">Latest: v0.3.0</span> -> <span class="version-tag">Latest: v0.2.2</span>
    """
    pattern = r'(<span class="version-tag">Latest:\s*v)[0-9\.]+(</span>)'
    replacement = rf'\g<1>{new_version}\g<2>'
    return re.sub(pattern, replacement, content)

def update_json_version(content: str, new_version: str) -> str:
    """
    JSONコンテンツ内のバージョン表記を置換する関数
    例: "version": "0.3.0" -> "version": "0.2.2"
    """
    pattern = r'("version"\s*:\s*")[0-9\.]+(")'
    replacement = rf'\g<1>{new_version}\g<2>'
    return re.sub(pattern, replacement, content)

def get_current_version(version_file_path: str) -> str:
    """
    version.py から VERSION 変数の値を読み取る
    """
    with open(version_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'VERSION\s*=\s*"([^"]+)"', content)
    if match:
        return match.group(1)
    raise ValueError("Version string not found in version.py")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    version_file = os.path.join(base_dir, 'src', 'version.py')
    
    try:
        new_version = get_current_version(version_file)
        print(f"Current version found: {new_version}")
    except Exception as e:
        print(f"Error reading version.py: {e}")
        return

    # Update index.html
    html_file = os.path.join(base_dir, 'docs', 'index.html')
    if os.path.exists(html_file):
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        updated_html = update_html_version(html_content, new_version)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated_html)
        print(f"Updated {html_file}")
    else:
        print(f"File not found: {html_file}")

    # Update stats.json
    json_file = os.path.join(base_dir, 'docs', 'stats.json')
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            json_content = f.read()
        
        updated_json = update_json_version(json_content, new_version)
        
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(updated_json)
        print(f"Updated {json_file}")
    else:
        print(f"File not found: {json_file}")

if __name__ == "__main__":
    main()
