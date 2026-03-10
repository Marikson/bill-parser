class Water:
    def __init__(self):
        self.sewer_data = {
            "Sewer": 0,
        }
        self.water_data = {
            "Cold water": 0,
        }


    def get_water_data(self, line):
        parts = line.split(':')
        if len(parts) == 2:
            parts[-1] = parts[-1].replace(' Ft', '').strip()
            val = parts[-1]
            return val

    def process_sewer(self, text, filename):
        print(f"Processing {filename}...")
        if text.get('content'):
            lines = [line.strip() for line in text['content'].split('\n') if line.strip()]
            for line in lines:
                if "Fizetendő összeg" in line:
                    val = self.get_water_data(line)
                    if val:
                        self.sewer_data['Sewer'] = val
            if self.sewer_data['Sewer'] == 0:
                print(f"Sewer data not found in {filename}")
            print("="*150)


    def process_water(self, text, filename):
        print(f"Processing {filename}...")
        if text.get('content'):
            lines = [line.strip() for line in text['content'].split('\n') if line.strip()]
            for line in lines:
                if "Fizetendő összeg:" in line:
                    val = self.get_water_data(line)
                    if val:
                        self.water_data['Cold water'] = val
                    else:
                        print(f"Could not parse water data from line: {line}")
            if self.water_data['Cold water'] == 0:
                print(f"Cold water data not found in {filename}")
            print("="*150)