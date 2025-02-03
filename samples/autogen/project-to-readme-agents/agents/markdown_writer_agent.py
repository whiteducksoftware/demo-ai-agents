from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

AGENT_NAME = "MarkdownWriter"
AGENT_INSTRUCTIONS = """
You are a helpful markdown writer. Respond with valid and well-formatted markdown content.
"""


class MarkdownWriterAgent(AssistantAgent):
    """
    An agent that reads a file from the system and returns its content.
    """

    def __init__(self, name: str, model_client: ChatCompletionClient):
        super().__init__(name, model_client, description=AGENT_INSTRUCTIONS)
