# src/my_project/crew.py
from typing import List

from crewai_tools import SerperDevTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

@CrewBase
class MyAgent():
    """LatestAiDevelopment crew"""
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        """
        Researcher agent
        """
        return Agent(
			config=self.agents_config['researcher'],
			verbose=True,
			tools=[SerperDevTool()]
		)

    @agent
    def reporting_analyst(self) -> Agent:
        """
        Reporting Analyst agent
        """
        return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

    @task
    def research_task(self) -> Task:
        """
        Research task
        """
        return Task(
			config=self.tasks_config['research_task'],
		)

    @task
    def reporting_task(self) -> Task:
        """
        Reporting task
        """
        return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
