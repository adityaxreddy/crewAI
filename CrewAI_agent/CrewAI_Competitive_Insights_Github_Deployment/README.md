# Competitive Insights Generator Crew

Welcome to the Competitive Insights Generator Crew project. This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
uv lock
```
```bash
uv sync
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/competitive_insights_generator/config/agents.yaml` to define your agents
- Modify `src/competitive_insights_generator/config/tasks.yaml` to define your tasks
- Modify `src/competitive_insights_generator/crew.py` to add your own logic, tools and specific args
- Modify `src/competitive_insights_generator/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```


This command initializes the competetive_insights_generator Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.



