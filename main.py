import csv
import json
import os

def parse_medicine_csv_to_json(csv_path, json_path):
    """
    Parses the Bangladeshi medicine dataset into a clean JSON array.
    Cleans up string artifacts, trailing quotes, and explicitly casts numerical values.
    """
    if not os.path.exists(csv_path):
        print(f"Error: Target file '{csv_path}' not found.")
        return

    medicines = []

    print(f"Opening and parsing '{csv_path}'...")
    # 'utf-8-sig' handles Excel Byte Order Marks automatically
    with open(csv_path, mode='r', encoding='utf-8-sig') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row_index, row in enumerate(reader, start=1):
            # Clean string fields by stripping extra whitespaces and escaping layout anomalies
            cleaned_row = {}
            for k, v in row.items():
                if k and v:
                    # Strip spaces and clear excessive double-quote maps from scraped files
                    cleaned_row[k.strip()] = v.strip().replace('"""', '').replace('"', '')
                else:
                    cleaned_row[k.strip()] = ""

            # Check if it's the broken period data row, bypass empty slots gracefully
            if cleaned_row.get("manufacturer_name") == ".":
                cleaned_row["manufacturer_name"] = "N/A"

            # Safely transform numeric values to prevent standard JSON structural errors
            try:
                unit_size = int(cleaned_row.get("unit_size", 1))
            except ValueError:
                unit_size = 1

            try:
                price = float(cleaned_row.get("price", 0.0))
            except ValueError:
                price = 0.0

            # Organize the final structured entity object map
            med_entry = {
                "medicine_name": cleaned_row.get("medicine_name", ""),
                "category_name": cleaned_row.get("category_name", ""),
                "slug": cleaned_row.get("slug", ""),
                "generic_name": cleaned_row.get("generic_name", ""),
                "strength": cleaned_row.get("strength", ""),
                "manufacturer_name": cleaned_row.get("manufacturer_name", ""),
                "unit": cleaned_row.get("unit", ""),
                "unit_size": unit_size,
                "price_bdt": price
            }
            
            medicines.append(med_entry)

    print(f"Saving compiled structure to '{json_path}'...")
    with open(json_path, mode='w', encoding='utf-8') as json_file:
        # indent=2 outputs clean visual blocks
        # ensure_ascii=False saves native signs (like micrograms 'mcg/µg' and brackets) correctly
        json.dump(medicines, json_file, indent=2, ensure_ascii=False)

    print(f"Conversion complete! Processed {len(medicines)} medicine items.")

# --- EXECUTION MAPPING ---
# 1. Save your data raw string block as 'medicines.csv'
# 2. Run this python file in the same directory path terminal.
if __name__ == "__main__":
    parse_medicine_csv_to_json('medicines.csv', 'medicines.json')
