"""main.py"""
from crew import MyAgent

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI Agents'
    }

    agent = MyAgent()
    agent.crew().kickoff(inputs=inputs)
