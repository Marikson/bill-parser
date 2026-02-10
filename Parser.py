import Garbage
import CommonCost
import Electricity
import Water
import Internet
import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tika import parser


def get_pdf_contents(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            pdf_text = parser.from_file(file_path)
            if "common_cost" in filename:
                CommonCost.process_common_cost(pdf_text, filename)
            elif "garbage" in filename:
                Garbage.process_garbage(pdf_text, filename)
            elif "electricity" in filename:
                Electricity.process_electricity(pdf_text, filename)
            elif "water" in filename:
                Water.process_water(pdf_text, filename)
            elif "sewer" in filename:
                Water.process_sewer(pdf_text, filename)
            elif "internet" in filename:
                Internet.process_internet(pdf_text, filename)
            else:
                print(f"Unknown file type for {filename}. Skipping...\n")

    

def write_summary_to_file(filename="summary.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            # Common cost
            f.write("Common cost:\n")
            f.write(f"  Price: {CommonCost.common_cost_data.get('Common Cost', '')}\n\n")
            f.write("Service fee:\n")
            f.write(f"  Price: {CommonCost.common_cost_data.get('Service fee', '')}\n\n")
            # Hot water
            f.write("Hot water:\n")
            for key in ["Price/m3", "Previous standing", "Current standing", "Consumption", "Price"]:
                val = CommonCost.common_cost_data["Hot Water"].get(key, "")
                if val is not None:
                    f.write(f"  {key}: {val}\n")
                else:
                    f.write(f"  {key}: N/A\n")
            f.write("\n")
            # Heating
            f.write("Heating:\n")
            for key in ["Price/KWh", "Previous standing", "Current standing", "Consumption", "Price"]:
                val = CommonCost.common_cost_data["Heating"].get(key, "")
                if val is not None:
                    f.write(f"  {key}: {val}\n")
                else:
                    f.write(f"  {key}: N/A\n")
            f.write("\n")
            # Electricity
            f.write("Electricity:\n")
            for key in ["Previous standing", "Current standing", "Consumption", "Price"]:
                val = Electricity.electricity_data.get(key, "")
                if val is not None:
                    f.write(f"  {key}: {val}\n")
                else:
                    f.write(f"  {key}: N/A\n")
            f.write("\n")
            # All together
            f.write("All together:\n")
            all_costs = [
                ("  Common cost", CommonCost.common_cost_data.get("Common Cost", 0)),
                ("  Service fee", CommonCost.common_cost_data.get("Service fee", 0)),
                ("  Hot water", CommonCost.common_cost_data["Hot Water"].get("Price", 0)),
                ("  Heating", CommonCost.common_cost_data["Heating"].get("Price", 0)),
                ("  Electricity", Electricity.electricity_data.get("Price", 0)),
                ("  Garbage", Garbage.garbage_data.get("Garbage", 0)),
                ("  Internet", Internet.internet_data.get("Internet", 0)),
                ("  Cold water", Water.water_data.get("Cold water", 0)),
                ("  Sewer", Water.sewer_data.get("Sewer", 0)),
            ]
            total = 0
            for label, value in all_costs:
                try:
                    int_val = int(str(value).replace(" ", "")) if value else 0
                except ValueError:
                    int_val = 0
                total += int_val
                f.write(f"{label}: {value}\n")
            # Write the total in bold using Markdown syntax
            f.write("\n**Summa: {:,}**\n".format(total).replace(",", " "))



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python pdf_parser.py <folder_path>")
        sys.exit(1)
    folder = sys.argv[1]
    get_pdf_contents(folder)
    print("Processing completed.")
    current_month = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")
    write_summary_to_file(folder + '/' + current_month + "_summary.txt")

    


