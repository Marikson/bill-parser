class Electricity:
    def __init__(self):
        self.electricity_data = {
            "Previous standing": None,
            "Current standing": None,
            "Consumption": None,
            "Price": 0,      
        }

    def get_electricity_data(self,line):
        parts = line.split()
        if len(parts) == 8:
            vals = [parts[2].replace('.',' '), parts[3].replace('.',' '), parts[-1]]
            return vals
        elif len(parts) == 4:
            vals = [parts[-1].replace('.',' ')]
            return vals
        
    
    def process_electricity(self, text, filename):
        print(f"Processing {filename}...")
        if text.get('content'):
            lines = [line.strip() for line in text['content'].split('\n') if line.strip()]
            for line in lines:
                if "9901121662" in line:          
                    vals = self.get_electricity_data(line)
                    self.electricity_data['Previous standing'] = vals[0]
                    self.electricity_data['Current standing'] = vals[1]
                    self.electricity_data['Consumption'] = vals[2]
                elif "Fizetendő összeg összesen" in line:
                    vals = self.get_electricity_data(line)
                    if vals:
                        self.electricity_data['Price'] = vals[0]
                    else:
                        print(f"Could not parse electricity price from line: {line}")
            print("="*150)