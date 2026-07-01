"""Base Agent class mimicking the Agent Development Kit (ADK) pattern."""

class Agent:
    def __init__(self, name: str):
        self.name = name

    def run(self, input_data):
        raise NotImplementedError("Subclasses must implement run()")