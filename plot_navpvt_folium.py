import pandas as pd
import folium
import sys
import os

def format_popup(row):
    return (
        f"<b>Timestamp:</b> {row['timestamp']}<br>"
        f"<b>Latitude:</b> {row['latitude']:.7f}<br>"
        f"<b>Longitude:</b> {row['longitude']:.7f}<br>"
        f"<b>Altitude:</b> {row['altitude']} m<br>"
        f"<b>Fix Type:</b> {row['fix_type']}<br>"
        f"<b>Flags:</b> {row['flags']}<br>"
        f"<b>Satellites:</b> {row['num_sv']}<br>"
        f"<b>Speed:</b> {row['ground_speed_mps']} m/s<br>"
        f"<b>Heading:</b> {row['heading_deg']}°"
    )

def plot_navpvt_on_map(csv_file):
    df = pd.read_csv(csv_file)

    if df.empty:
        print("CSV is empty. Nothing to plot.")
        return

    # 緯度・経度のリスト
    path = list(zip(df['latitude'], df['longitude']))

    # 中心位置（最初の座標）
    start_lat, start_lon = path[0]

    # 地図作成
    fmap = folium.Map(location=[start_lat, start_lon], zoom_start=17)

    # 軌跡のPolyline
    folium.PolyLine(path, color='blue', weight=3, opacity=0.6).add_to(fmap)

    # 各観測点に詳細ポップアップをつけたマーカー
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=3,
            color='green',
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(format_popup(row), max_width=300)
        ).add_to(fmap)

    # 開始・終了マーカー
    folium.Marker(path[0], popup="Start", icon=folium.Icon(color='green')).add_to(fmap)
    folium.Marker(path[-1], popup="End", icon=folium.Icon(color='red')).add_to(fmap)

    # 保存
    output_html = os.path.splitext(csv_file)[0] + "_detailed_map.html"
    fmap.save(output_html)
    print(f"Map saved to {output_html}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plot_navpvt_folium_detailed.py navpvt_data.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    plot_navpvt_on_map(csv_path)

