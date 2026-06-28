# Simple Cycle Engine (safe version)

class CycleEngine:
    def __init__(self, config=None):
        self.config = config or {}
        self.state = {}

    def initialize(self):
        """Initialize engine state"""
        self.state["status"] = "initialized"
        return self.state

    def step(self, input_data=None):
        """Single computation step"""
        input_data = input_data or {}

        # simple processing logic (placeholder)
        result = {
            "input": input_data,
            "processed": True,
            "status": "running"
        }

        self.state.update(result)
        return result

    def run(self, steps=1, input_data=None):
        """Run multiple steps"""
        output = None

        for i in range(steps):
            output = self.step(input_data)

        self.state["status"] = "completed"
        return output


# اگر مستقیم اجرا شد
if __name__ == "__main__":
    engine = CycleEngine()
    engine.initialize()
    result = engine.run(steps=3, input_data={"test": 123})
    print(result)
