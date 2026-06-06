import re
from datetime import datetime

class CommonCost:
    service_fee_pattern = rf"{datetime.now().year}.*Rendelkezésre állási díj"
    renovation_fee_pattern = rf"{datetime.now().year}.*Felújítási alap"

    common_cost_data = {
        "Common Cost": None,
        "int_Common Cost": None,
        "Service fee": 0,
        "Renovation fee": 0,
        "Reimbursement": 0,
            "Hot Water": {
                "Price/m3": None,
                "Previous standing": None,
                "Current standing": None,
                "Consumption": None,
                "Price": 0,
            },
            "Heating": {
                "Price/KWh": None,
                "Previous standing": None,
                "Current standing": None,
                "Consumption": None,
                "Price": 0,
            }
        }

    
    def get_parsed_line_val(self, line, member_index=2):
        parts = re.split(r'\s{2,}', line)
        if len(parts) == 4:
            val = parts[member_index]
            return val

   
    def process_common_cost(self, text, filename):
        print(f"Processing {filename}...")
        if text.get('content'):
            lines = [line.strip() for line in text['content'].split('\n') if line.strip()]
            for line in lines:
                if "Közös költség" in line:
                    val = self.get_parsed_line_val(line, 2)
                    if val:
                        self.common_cost_data['Common Cost'] = val
                elif re.search(self.service_fee_pattern, line):
                    val = self.get_parsed_line_val(line, 2)
                    if val:
                        self.common_cost_data['Service fee'] = val
                    else:
                        print(f"Could not parse service fee from line: {line}")
                elif re.search(self.renovation_fee_pattern, line):
                    val = self.get_parsed_line_val(line, 2)
                    if val:
                        self.common_cost_data['Renovation fee'] = val
                    else:
                        print(f"Could not parse renovation fee from line: {line}")
                elif "Melegvíz egységár" in line:
                    self.set_detailed_vals(line, column="Hot Water", unit="Price/m3")
                elif "Fűtési egységár" in line:
                    self.set_detailed_vals(line, column="Heating", unit="Price/KWh")
                elif "Rezsicsökkentés" in line:
                    val = self.get_parsed_line_val(line, 3)
                    if val:
                        self.common_cost_data['Reimbursement'] = val
                    else:
                        print(f"Could not parse reimbursement from line: {line}")
            if self.common_cost_data['Common Cost'] is None:
                print(f"Common cost data not found in {filename}")
            if self.common_cost_data['Service fee'] == 0:
                print(f"Service fee data not found in {filename}")
            if self.common_cost_data['Renovation fee'] == 0:
                print(f"Renovation fee data not found in {filename}")
            if self.common_cost_data['Hot Water']['Price'] == 0:
                print(f"Hot water price data not found in {filename}")
            if self.common_cost_data['Heating']['Price'] == 0:
                print(f"Heating price data not found in {filename}")
            print("="*150)


    def set_detailed_vals(self, line, column, unit):
        parts = re.split(r'\s{2,}', line)
        if len(parts) == 2:
            self.common_cost_data[column][unit] = parts[1]
        elif len(parts) == 5:
            self.common_cost_data[column]['Previous standing'] = (parts[1])
            self.common_cost_data[column]['Current standing'] = (parts[2])
            self.common_cost_data[column]['Consumption'] = (parts[3])
            self.common_cost_data[column]['int_Price'] = int(parts[4].replace(' ', ''))  # Remove spaces in price
            self.common_cost_data[column]['Price'] = parts[4]
