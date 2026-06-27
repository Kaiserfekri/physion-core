import json

class ParameterSet:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def from_json(path):
        with open(path, "r") as f:
            data = json.load(f)
        return ParameterSet(data)

    def __getitem__(self, key):
        return self.data[key]
