import sys
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tika import parser

from Garbage import Garbage
from CommonCost import CommonCost
from Electricity import Electricity
from Water import Water
from Internet import Internet


class Parser:
    def get_pdf_contents(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.pdf'):
                file_path = os.path.join(folder_path, filename)
                pdf_text = parser.from_file(file_path)
                if "common_cost" in filename:
                    self.common_cost_instance = CommonCost()
                    self.common_cost_instance.process_common_cost(pdf_text, filename)
                elif "garbage" in filename:
                    self.garbage_instance = Garbage()
                    self.garbage_instance.process_garbage(pdf_text, filename)
                elif "electricity" in filename:
                    self.electricity_instance = Electricity()
                    self.electricity_instance.process_electricity(pdf_text, filename)
                elif "water" in filename:
                    self.cold_water_instance = Water()
                    self.cold_water_instance.process_water(pdf_text, filename)
                elif "sewer" in filename:
                    self.sewer_instance = Water()
                    self.sewer_instance.process_sewer(pdf_text, filename)
                elif "internet" in filename:
                    self.internet_instance = Internet()
                    self.internet_instance.process_internet(pdf_text, filename)
                else:
                    print(f"Unknown file type for {filename}. Skipping...\n")

        

    def write_summary_to_file(self, filename="summary.txt"):
            with open(filename, "w", encoding="utf-8") as f:
                # Common cost
                if hasattr(self, 'common_cost_instance'):
                    f.write("Common cost:\n")
                    f.write(f"  Price: {self.common_cost_instance.common_cost_data.get('Common Cost', '')}\n\n")
                    f.write("Service fee:\n")
                    f.write(f"  Price: {self.common_cost_instance.common_cost_data.get('Service fee', '')}\n\n")
                    f.write("Reimbursement:\n")
                    f.write(f"  Amount: {self.common_cost_instance.common_cost_data.get('Reimbursement', '')}\n\n")
                    f.write("Renovation fee:\n")
                    f.write(f"  Amount: {self.common_cost_instance.common_cost_data.get('Renovation fee', '')}\n\n")
                # Hot water
                f.write("Hot water:\n")
                for key in ["Price/m3", "Previous standing", "Current standing", "Consumption", "Price"]:
                    val = self.common_cost_instance.common_cost_data["Hot Water"].get(key, "") if hasattr(self, 'common_cost_instance') else None
                    if val is not None:
                        f.write(f"  {key}: {val}\n")
                    else:
                        f.write(f"  {key}: N/A\n")
                f.write("\n")
                # Heating
                f.write("Heating:\n")
                for key in ["Price/KWh", "Previous standing", "Current standing", "Consumption", "Price"]:
                    val = self.common_cost_instance.common_cost_data["Heating"].get(key, "") if hasattr(self, 'common_cost_instance') else None
                    if val is not None:
                        f.write(f"  {key}: {val}\n")
                    else:
                        f.write(f"  {key}: N/A\n")
                f.write("\n")
                # Electricity
                f.write("Electricity:\n")
                for key in ["Previous standing", "Current standing", "Consumption", "Price"]:
                    val = self.electricity_instance.electricity_data.get(key, "") if hasattr(self, 'electricity_instance') else None
                    if val is not None:
                        f.write(f"  {key}: {val}\n")
                    else:
                        f.write(f"  {key}: N/A\n")
                f.write("\n")
                # All together
                f.write("All together:\n")
                all_costs = [
                    ("  Common cost", self.common_cost_instance.common_cost_data.get("Common Cost", 0)) if hasattr(self, 'common_cost_instance') else ("  Common cost", 0),
                    ("  Service fee", self.common_cost_instance.common_cost_data.get("Service fee", 0)) if hasattr(self, 'common_cost_instance') else ("  Service fee", 0),
                    ("  Reimbursement", self.common_cost_instance.common_cost_data.get("Reimbursement", 0)) if hasattr(self, 'common_cost_instance') else ("  Reimbursement", 0),
                    ("  Renovation fee", self.common_cost_instance.common_cost_data.get("Renovation fee", 0)) if hasattr(self, 'common_cost_instance') else ("  Renovation fee", 0),
                    ("  Hot water", self.common_cost_instance.common_cost_data["Hot Water"].get("Price", 0)) if hasattr(self, 'common_cost_instance') else ("  Hot water", 0),
                    ("  Heating", self.common_cost_instance.common_cost_data["Heating"].get("Price", 0)) if hasattr(self, 'common_cost_instance') else ("  Heating", 0),
                    ("  Electricity", self.electricity_instance.electricity_data.get("Price", 0)) if hasattr(self, 'electricity_instance') else ("  Electricity", 0),
                    ("  Garbage", self.garbage_instance.garbage_data.get("Garbage", 0)) if hasattr(self, 'garbage_instance') else ("  Garbage", 0),
                    ("  Internet", self.internet_instance.internet_data.get("Internet", 0)) if hasattr(self, 'internet_instance') else ("  Internet", 0),
                    ("  Cold water", self.cold_water_instance.water_data.get("Cold water", 0)) if hasattr(self, 'cold_water_instance') else ("  Cold water", 0),
                    ("  Sewer", self.sewer_instance.sewer_data.get("Sewer", 0)) if hasattr(self, 'sewer_instance') else ("  Sewer", 0),
                ]
                total = 0
                for label, value in all_costs:
                    try:
                        int_val = int(str(value).replace(" ", "")) if value else 0
                    except ValueError:
                        int_val = 0
                    if label.strip() == "Reimbursement":
                        int_val = -int_val  # Subtract reimbursement from total
                    total += int_val
                    f.write(f"{label}: {value}\n")
                # Write the total in bold using Markdown syntax
                f.write("\n**Summa: {:,}**\n".format(total).replace(",", " "))



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python pdf_parser.py <folder_path>")
        sys.exit(1)
    folder = sys.argv[1]

    bill_parser = Parser()
    bill_parser.get_pdf_contents(folder)
    print("Processing completed.")
    current_month = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")
    bill_parser.write_summary_to_file(folder + '/' + current_month + "_summary.txt")

    


