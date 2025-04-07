from crewai_tools import SerperDevTool

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class CompetitiveInsightsGenerator:
    """Competitive Insights Generator crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def competitive_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["competitive_researcher"],
            tools=[SerperDevTool()],
            allow_delegation=True,
            verbose=True,
        )

    @agent
    def insights_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["insights_writer"],
            tools=[SerperDevTool()],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["analysis_task"],
            tools=[SerperDevTool()],
            async_execution=False,
            agent=self.competitive_researcher(),
        )

    @task
    def insights_task(self) -> Task:
        return Task(
            config=self.tasks_config["insights_task"],
            tools=[SerperDevTool()],
            agent=self.insights_writer(),
            async_execution=False,
            context=[self.analysis_task()],
            output_file="competitive_insights.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Competitive Insights Generator"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
