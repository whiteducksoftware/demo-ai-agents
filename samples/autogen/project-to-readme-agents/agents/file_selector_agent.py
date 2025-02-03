from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

AGENT_NAME = "FileSelector"
AGENT_INSTRUCTIONS = """
You are a helpful AI assistant tasked with analyzing a Python project's file structure to determine which files are essential for creating a comprehensive README.md file. 
Focus on identifying configuration files (e.g., pyproject.toml), environment files (e.g., .env), and any other relevant files that provide key insights into the project's setup, 
dependencies, and usage. Also use any source files e. g. .py files to extract information about the project.
"""


class FileSelectorAgent(AssistantAgent):
    """
    An agent that reads a file from the system and returns its content.
    """

    def __init__(self, name: str, model_client: ChatCompletionClient):
        super().__init__(name, model_client, description=AGENT_INSTRUCTIONS)
