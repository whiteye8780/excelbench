import sys
import os

# Add scripts directory to path to import update_version
scripts_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts')
sys.path.insert(0, scripts_dir)

from update_version import update_html_version, update_json_version

def test_update_html_version():
    content = '<div class="cta-group"><a href="#download" class="btn-large">無料診断を開始</a><span class="version-tag">Latest: v0.3.0</span></div>'
    new_version = "1.2.3"
    expected = '<div class="cta-group"><a href="#download" class="btn-large">無料診断を開始</a><span class="version-tag">Latest: v1.2.3</span></div>'
    
    assert update_html_version(content, new_version) == expected

def test_update_html_version_no_match():
    content = '<div>No version here</div>'
    new_version = "1.2.3"
    expected = '<div>No version here</div>'
    
    assert update_html_version(content, new_version) == expected

def test_update_json_version():
    content = '{\n    "last_update": "2026-03-12",\n    "version": "0.3.0",\n    "global_average": 8.4\n}'
    new_version = "1.2.3"
    expected = '{\n    "last_update": "2026-03-12",\n    "version": "1.2.3",\n    "global_average": 8.4\n}'
    
    assert update_json_version(content, new_version) == expected

if __name__ == "__main__":
    test_update_html_version()
    test_update_html_version_no_match()
    test_update_json_version()
    print("All tests passed successfully.")
