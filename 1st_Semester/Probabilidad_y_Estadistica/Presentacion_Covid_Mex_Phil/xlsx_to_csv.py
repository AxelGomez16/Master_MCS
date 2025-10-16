import pandas as pd
import os
import glob


def convert_xlsx_to_csv_folder(folder_path, output_folder=None):
  if output_folder is None:
    output_folder = folder_path

  os.makedirs(output_folder, exist_ok=True)

  xlsx_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

  if not xlsx_files:
    print(f"No XLSX files found in '{folder_path}'")
    return

  print(f"Found {len(xlsx_files)} XLSX file(s) to convert...")

  success_count = 0
  error_count = 0

  for xlsx_file in xlsx_files:
    try:
      base_name = os.path.splitext(os.path.basename(xlsx_file))[0]
      csv_file = os.path.join(output_folder, f"{base_name}.csv")
      df = pd.read_excel(xlsx_file)

      df.to_csv(csv_file, index=False)

      print(f"Converted: {os.path.basename(xlsx_file)} -> {os.path.basename(csv_file)}")
      success_count += 1

    except Exception as e:
      print(f"Failed to convert {os.path.basename(xlsx_file)}: {e}")
      error_count += 1

  print(f"\nConversion completed: {success_count} successful, {error_count} failed")


if __name__ == "__main__":
  folder_path = r"./"
  output_folder = r"./"

  convert_xlsx_to_csv_folder(folder_path, output_folder)