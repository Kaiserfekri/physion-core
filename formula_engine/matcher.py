import re

class FormulaMatcher:
    SIMPLE_PATTERNS = {
        "li_metal_interface": [
            r"i\s*=\s*V/R",
            r"J\s*=\s*k\*c",
        ],
        "sei_growth": [
            r"dL_sei\s*=\s*k\*i",
        ],
    }

    def find_simple_formulas(self, text, topic):
        patterns = self.SIMPLE_PATTERNS.get(topic, [])
        hits = []
        for p in patterns:
            if re.search(p, text):
                hits.append(p)
        return hits
