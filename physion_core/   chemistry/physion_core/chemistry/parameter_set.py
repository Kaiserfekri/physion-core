import json

class ParameterSet:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def from_json(path: str) -> "ParameterSet":
        with open(path, "r") as f:
            data = json.load(f)
        ps = ParameterSet(data)
        ps.validate()
        return ps

    def __getitem__(self, key):
        return self.data[key]

    def validate(self):
        if not isinstance(self.data, dict):
            raise ValueError("ParameterSet data must be a dict.")
