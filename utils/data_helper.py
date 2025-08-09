import random
import pandas as pd

class DataHelper:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()
        self.used_words = {section: set() for section in self.data}

    def load_data(self):
        all_sheets = pd.read_excel(self.file_path, sheet_name=None)
        data = {}
        for sheet_name, df in all_sheets.items():
            filtered = df[df['Status'] == 1]['Word'].tolist()
            data[sheet_name] = filtered
        return data

    def get_random_words(self, section, n):
        available = [w for w in self.data[section] if w not in self.used_words[section]]
        if len(available) < n:
            n = len(available)  # Only take what's left for verbs
        selected = random.sample(available, min(n, len(available)))
        return selected

    def get_words(self, words_per_section):
        # get verbs
        available_verbs = [w for w in self.data["Verbs"] if w not in self.used_words["Verbs"]]
        n_verbs_per_section = words_per_section["Verbs"]
        n = 1
        if len(available_verbs) <= 0:
            print("No more unused verbs available.")
            return {}
        
        selected_verbs = random.sample(available_verbs, min(n, n_verbs_per_section))
        
        selected_data = {"Verbs": selected_verbs}
        self.used_words["Verbs"].update(selected_verbs)
        
        for section, n_words in words_per_section.items():
            if section == "Verbs":
                continue
            if section not in self.data or n_words < 1:
                continue
            
            available = [w for w in self.data[section] if w not in self.used_words[section]]
            if len(available) <= 0:
                self.used_words[section]= set()  # Reset used words if none are available
                available = [w for w in self.data[section] if w not in self.used_words[section]]
            
            if len(available) < n:
                n = len(available)  # Only take what's left for verbs
            selected = random.sample(available, min(n, len(available)))
            selected_data[section] = selected
            self.used_words[section].update(selected)
        return selected_data

if __name__ == "__main__":

    # Replace with your Excel file path
    file_path = "english_business.xlsx"
    data_helper = DataHelper(file_path)
    words_per_section = {"Verbs":1, "Connectors":1, "Nouns":1, "Questions":1, "Phrases":1, "Times":1, "Misc":1}

    i = 0
    while True:

        selected_words = data_helper.get_words(words_per_section)
        if not selected_words:
            print("No more words available. Exiting.")
            break
        print("---------------- Selected Words --------------")
        print(f"Iteration {i + 1}")
        i += 1
        # Print the rest, skipping "Verbs"
        for section, words in selected_words.items():
            print(f"{section}: {', '.join(words)}")