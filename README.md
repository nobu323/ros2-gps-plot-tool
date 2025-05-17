# 📍 navpvt\_tools

このリポジトリは、ROS2のrosbag2ファイル（`.db3` または `.mcap`）から `/navpvt` トピックのGPSデータを抽出し、Foliumを使って可視化するツールセットです。

---

## 📦 ファイル構成

* `extract_navpvt.py`
  `.db3` または `.mcap` 形式のrosbag2ファイルから、`/navpvt` トピックのGPSデータをCSV形式で抽出します。

* `plot_navpvt_folium.py`
  上記で生成されたCSVをもとに、Folium地図上に軌跡と各観測点の詳細情報をプロットしたHTMLマップを作成します。

---

## 🧰 必要なライブラリ

以下のPythonパッケージが必要です：

```bash
pip install pandas folium
```

また、`extract_navpvt.py` を使用するには、ROS2環境がセットアップされており、以下のPythonパッケージが使える必要があります：

* `rosbag2_py`
* `rclpy`
* `rosidl_runtime_py`

---

## 🚀 使用方法

### 1. GPSデータの抽出

```bash
python3 extract_navpvt.py <rosbag2_directory>
```

例：

```bash
python3 extract_navpvt.py /path/to/rosbag2_2024_12_08-06_12_13/
```

* 入力: `rosbag2_2024_12_08-06_12_13/` ディレクトリ内に `.db3` または `.mcap` ファイルが含まれている必要があります。
* 出力: `rosbag2_2024_12_08-06_12_13_fix.csv` が生成されます。

---

### 2. 地図へのプロット

```bash
python3 plot_navpvt_folium.py <csv_file>
```

例：

```bash
python3 plot_navpvt_folium.py rosbag2_2024_12_08-06_12_13_fix.csv
```

* 入力: `*_fix.csv` ファイル（上記ステップで生成）
* 出力: `*_fix_detailed_map.html` が同ディレクトリに生成されます。

---

## 🧱 出力されるCSVのカラム

| カラム名               | 説明             |
| ------------------ | -------------- |
| timestamp          | ROSタイムスタンプ（ns） |
| latitude           | 緯度（°）          |
| longitude          | 経度（°）          |
| altitude           | 高度（m）          |
| fix\_type          | GNSSフィックスのタイプ  |
| flags              | フラグ（精度・状態など）   |
| num\_sv            | 可視衛星数          |
| ground\_speed\_mps | 地表速度（m/s）      |
| heading\_deg       | 方位角（度）         |

---

## 🌐 出力されるHTMLマップ

出力されたマップ（`.html`）では以下の情報が表示されます：

* ロボットの走行軌跡（青線）
* 各ポイントの詳細（クリックするとポップアップ）
* 開始地点（緑）と終了地点（赤）のマーカー

---

## 📲 お問い合わせ

何か問題が発生した場合や機能追加のご要望がある場合は、お気軽にIssueまたはPRを送ってください。
