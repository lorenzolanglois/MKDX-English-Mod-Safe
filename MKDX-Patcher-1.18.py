import csv
import os

files_folder = input("Enter path to the \"files-1.18\" folder (you can drop it): ").strip("\"")
data_folder = input("Enter path to the \"data_jp\" folder (you can drop it): ").strip("\"")
csv_file = os.path.join(files_folder, "files.csv")
backup_folder = os.path.join(data_folder, "backup")
os.makedirs(backup_folder, exist_ok=True)

with open(csv_file, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        relative_target = os.path.relpath(row["target"], "Data/flash/data_jp")
        target_path = os.path.normpath(os.path.join(data_folder, relative_target))
        dds_path = os.path.normpath(os.path.join(files_folder, row["file"]))
        offset_value = row["offset"].strip().lower()

        if not os.path.exists(dds_path):
            print(f"Missing: {dds_path}")
            continue

        with open(dds_path, "rb") as dds_file:
            dds_data = dds_file.read()

        rel_target = os.path.relpath(target_path, data_folder)
        backup_path = os.path.join(backup_folder, rel_target)
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        if not os.path.exists(backup_path) and os.path.exists(target_path):
            with open(target_path, "rb") as original, open(backup_path, "wb") as backup:
                backup.write(original.read())

        if offset_value == "replace":
            with open(target_path, "wb") as f:
                f.write(dds_data)
            print(f"Replaced: {rel_target}")
        else:
            try:
                offset = int(offset_value)
            except ValueError:
                print(f"Invalid offset: {offset_value}")
                continue
            with open(target_path, "r+b") as f:
                f.seek(offset)
                f.write(dds_data)
            print(f"Patched: {rel_target}")

print("Done")
