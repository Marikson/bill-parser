class Garbage:
    def __init__(self):
        self.garbage_data = {
            "Garbage": 0,
        }
        
    def get_garbage_data(self, line):
        parts = line.split("FtFizetési mód")
        if len(parts) == 2:
            val = parts[0]
            return val


    def process_garbage(self, text, filename):
        print(f"Processing {filename}...")
        if text.get('content'):
            lines = [line.strip() for line in text['content'].split('\n') if line.strip()]
            for line in lines:
                if "Fizetési mód" in line:
                    val = self.get_garbage_data(line)
                    if val:
                        self.garbage_data['Garbage'] = val
                    else:
                        print(f"Could not parse garbage data from line: {line}")
            print("="*150) 