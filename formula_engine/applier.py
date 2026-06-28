import re
from .library import FormulaLibrary
from .matcher import FormulaMatcher

class FormulaApplier:
    def __init__(self):
        self.library = FormulaLibrary()
        self.matcher = FormulaMatcher()

    def upgrade_text(self, text, topic):
        simple_patterns = self.matcher.find_simple_formulas(text, topic)
        strong_formulas = self.library.get_formulas(topic)
        new_text = text
        for i, pattern in enumerate(simple_patterns):
            if i < len(strong_formulas):
                new_text = re.sub(pattern, strong_formulas[i], new_text)
        return new_text
