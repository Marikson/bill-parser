import re

class CommonCost:
    def __init__(self):
        self.common_cost_data = {
            "Common Cost": None,
            "int_Common Cost": None,
            "Service fee": 0,
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

    
    def get_parsed_line_val(line):
        parts = re.split(r'\s{2,}', line)
        if len(parts) == 4:
            val = parts[2]
            return val

   
    def process_common_cost(self, text, filename):
        print(f"Processing {filename}...")
        if text.get('content'):
            lines = [line.strip() for line in text['content'].split('\n') if line.strip()]
            for line in lines:
                if "Közös költség" in line:
                    val = self.get_parsed_line_val(line)
                    if val:
                        self.common_cost_data['Common Cost'] = val
                elif "Rendelkezésre állási díj" in line:
                    val = self.get_parsed_line_val(line)
                    if val:
                        self.common_cost_data['Service fee'] = val
                    else:
                        print(f"Could not parse service fee from line: {line}")
                elif "Melegvíz egységár" in line:
                    self.set_detailed_vals(line, column="Hot Water", unit="Price/m3")
                elif "Fűtési egységár" in line:
                    self.set_detailed_vals(line, column="Heating", unit="Price/KWh")
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
