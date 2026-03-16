# ExcelBench

[![Latest Release](https://img.shields.io/github/v/release/whiteye8780/excelbench)](https://github.com/whiteye8780/excelbench/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[日本語](#excelbench-jp) | [English](#excelbench-en)

---

<span id="excelbench-jp"></span>
## ExcelBench (JP)

**Excelの遅さは、利益の損失です。**

ExcelBenchは、日本特有の「重いExcel文化」を逆手に取り、PCの業務適正を可視化するベンチマークツールです。実務で使われる複雑な数式（RANDBETWEEN, COUNTIF等）を用いてハードウェアの限界を測定し、時間的損失を数値化します。

### 主な特徴
- **リアルな計測**: 実務に基づいた負荷テスト用ファイルを動的に生成して計測.
- **ROIの可視化**: 「年間で推定何時間の損失か」を具体的数値で提示.
- **マルチリンガル**: 日本語・英語に完全対応.
- **簡単操作**: インストール不要（ポータブル版）で、ワンクリック診断が可能.

### システム要件
- OS: Windows 10/11
- Microsoft Excel がインストールされていること

### ダウンロード
[最新リリースページ](https://github.com/whiteye8780/excelbench/releases)から `ExcelBench_vX.X.X.zip` をダウンロードしてください。

---

<span id="excelbench-en"></span>
## ExcelBench (EN)

**Excel slowness is a loss of profit.**

ExcelBench is a benchmark tool that visualizes your PC's business suitability by measuring Excel performance. It measures hardware limits using complex formulas (RANDBETWEEN, COUNTIF, etc.) and quantifies time loss.

### Key Features
- **Real-world Benchmarking**: Dynamically generates and measures load test files based on actual business scenarios.
- **ROI Visualization**: Presents specific impacts like "how many hours lost per year".
- **Multi-lingual**: Fully supports Japanese and English.
- **Easy Operation**: Portable (no installation required) and supports one-click diagnosis.

### System Requirements
- OS: Windows 10/11
- Microsoft Excel must be installed

### Download
Please download `ExcelBench_vX.X.X.zip` from the [Latest Releases Page](https://github.com/whiteye8780/excelbench/releases).

---

## Development Roadmap (Phase 1-6)

1. **Phase 1**: Core measurement logic with Python & pywin32. (Completed)
2. **Phase 2**: GUI implementation & Multi-lingual support. (In Progress)
3. **Phase 3**: GitHub Pages & stats.json delivery system.
4. **Phase 4**: Build distribution & Terms of Use.
5. **Phase 5**: Google Forms integration for stats.
6. **Phase 6**: Affiliate & Recommendation system.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
