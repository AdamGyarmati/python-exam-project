import json
from datetime import datetime


class WriteJsonData:
    def __init__(self, file):
        self._file = file

    def write_score(self, score):
        data = self.read_data()
        new_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
        }
        data.append(new_data)
        try:
            with open(self._file, "w") as json_file:
                json.dump(data, json_file, indent=4)
        except FileNotFoundError as e:
            print(e)

    def read_data(self):
        try:
            with open(self._file, "r") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            return []
