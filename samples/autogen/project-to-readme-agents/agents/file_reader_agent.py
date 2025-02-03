from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from autogen_core.models import ChatCompletionClient

AGENT_NAME = "FileReader"
AGENT_INSTRUCTIONS = """
You are a helpful AI assistant with file system access. 
When a user requests a file, locate and read the file from the system, then return its content. 
"""


async def read_file(file: str) -> str:
    # open the file and return the content
    with open(file, "r") as f:
        return f.read()


file_tool = FunctionTool(read_file, description="reads a file", name="file_reader")


class FileReaderAgent(AssistantAgent):
    """
    An agent that reads a file from the system and returns its content.
    """

    def __init__(self, name: str, model_client: ChatCompletionClient):
        super().__init__(
            name, model_client, description=AGENT_INSTRUCTIONS, tools=[file_tool]
        )
