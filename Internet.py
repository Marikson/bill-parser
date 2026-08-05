class Internet:
    def __init__(self):
        self.internet_data = {
            "Internet": 0,
        }


    def get_internet_data(self, line):
        parts = line.split()
        if len(parts) == 3:
            val = parts[-1].replace('.', ' ')
            return val
        
    
    def process_internet(self, text, filename):
        print(f"Processing {filename}...")
        if text.get('content'):
            lines = [line.strip() for line in text['content'].split('\n') if line.strip()]
            for line in lines:
                if "Mindösszesen" in line:
                    val = self.get_internet_data(line)
                    if val:
                        self.internet_data['Internet'] = val
                    else:
                        print(f"Could not parse internet data from line: {line}")
            if self.internet_data['Internet'] == 0:
                print(f"Internet data not found in {filename}")            
            print("="*150)