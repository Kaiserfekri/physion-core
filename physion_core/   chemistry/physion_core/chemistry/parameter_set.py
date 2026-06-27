import json

class ParameterSet:
    """
    نگه‌دارندهٔ پارامترهای شیمی (خوانده‌شده از JSON).
    """

    def __init__(self, data):
        self.data = data

    @staticmethod
    def from_json(path: str) -> "ParameterSet":
        with open(path, "r") as f:
            data = json.load(f)
        return ParameterSet(data)

    def __getitem__(self, key):
        return self.data[key]
