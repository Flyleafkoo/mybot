import json
import os

class LinkStorage:
    def __init__(self, file_path='sent_links.json'):
        self.file_path = file_path

    def load_sent_links(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return set(json.load(file))
        return set()

    def save_sent_links(self, sent_links):
        with open(self.file_path, 'w') as file:
            json.dump(list(sent_links), file)