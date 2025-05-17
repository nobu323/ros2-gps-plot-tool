import os
import sys
import sqlite3
import csv
import ast
from rosidl_runtime_py.utilities import get_message
from rclpy.serialization import deserialize_message
from rosbag2_py import StorageOptions, ConverterOptions
import re

def extract_from_db3(bag_path, db3_file, output_csv):
    db_path = os.path.join(bag_path, db3_file)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    topic_name = '/navpvt'
    cursor.execute(f"SELECT id, type FROM topics WHERE name='{topic_name}'")
    result = cursor.fetchone()
    if not result:
        print(f"Error: Topic '{topic_name}' not found in {db3_file}.")
        return

    topic_id, type_name = result
    msg_type = get_message(type_name)

    cursor.execute(f"SELECT timestamp, data FROM messages WHERE topic_id={topic_id}")
    rows = cursor.fetchall()

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'timestamp',
            'latitude',
            'longitude',
            'altitude',
            'fix_type',
            'flags',
            'num_sv',
            'ground_speed_mps',
            'heading_deg'
        ])

        for timestamp, data in rows:
            msg = deserialize_message(data, msg_type)
            writer.writerow([
                timestamp,
                msg.lat * 1e-7,
                msg.lon * 1e-7,
                msg.height * 1e-3,
                msg.fix_type,
                msg.flags,
                msg.num_sv,
                msg.g_speed * 1e-2,
                msg.heading * 1e-5
            ])
    print(f"✅ CSV written from DB3 to {output_csv}")

def extract_from_mcap(bag_path, mcap_file, output_csv):
    from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
    from rclpy.serialization import deserialize_message
    from rosidl_runtime_py.utilities import get_message

    reader = SequentialReader()

    # ✅ StorageOptionsは引数付きで構築する必要あり！
    storage_options = StorageOptions(
        uri=bag_path,
        storage_id='mcap'
    )

    converter_options = ConverterOptions(
        input_serialization_format='cdr',
        output_serialization_format='cdr'
    )

    reader.open(storage_options, converter_options)

    topic_types = reader.get_all_topics_and_types()
    type_dict = {t.name: t.type for t in topic_types}
    msg_type_str = type_dict.get('/navpvt', None)

    if not msg_type_str:
        print(f"Error:/navpvt topic not found in MCAP file.")
        return

    msg_type = get_message(msg_type_str)

    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'timestamp',
            'latitude',
            'longitude',
            'altitude',
            'fix_type',
            'flags',
            'num_sv',
            'ground_speed_mps',
            'heading_deg'
        ])

        while reader.has_next():
            (topic, data, t) = reader.read_next()
            if topic == '/navpvt':
                msg = deserialize_message(data, msg_type)
                writer.writerow([
                    t,
                    msg.lat * 1e-7,
                    msg.lon * 1e-7,
                    msg.height * 1e-3,
                    msg.fix_type,
                    msg.flags,
                    msg.num_sv,
                    msg.g_speed * 1e-2,
                    msg.heading * 1e-5
                ])

    print(f"✅ CSV written from MCAP to {output_csv}")


def main(bag_path):
    if not os.path.exists(bag_path):
        print("❌ Bag path does not exist.")
        return

    files = os.listdir(bag_path)
    db3_file = next((f for f in files if f.endswith(".db3")), None)
    mcap_file = next((f for f in files if f.endswith(".mcap")), None)
    bag_name = os.path.basename(bag_path.rstrip("/"))
    output_csv = f"{bag_name}_fix.csv"

    if db3_file:
        extract_from_db3(bag_path, db3_file, output_csv)
    elif mcap_file:
        extract_from_mcap(bag_path, mcap_file, output_csv)
    else:
        print("❌ No .db3 or .mcap file found in the given directory.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_gps_csv.py <rosbag2_directory>")
        sys.exit(1)

    main(sys.argv[1])