import pathlib
from formula_engine.applier import FormulaApplier

TOPIC_MAP = {
    "interface": "li_metal_interface",
    "sei": "sei_growth",
    "mech": "mechanical_coupling",
}

def detect_topic(file_path):
    name = file_path.name.lower()
    for key, topic in TOPIC_MAP.items():
        if key in name:
            return topic
    return "li_metal_interface"

def main():
    applier = FormulaApplier()
    for file in pathlib.Path("physion_core").rglob("*.py"):
        topic = detect_topic(file)
        text = file.read_text()
        new_text = applier.upgrade_text(text, topic)
        if new_text != text:
            file.write_text(new_text)
            print(f"[FormulaEngine] Upgraded formulas in {file} ({topic})")

if __name__ == "__main__":
    main()
