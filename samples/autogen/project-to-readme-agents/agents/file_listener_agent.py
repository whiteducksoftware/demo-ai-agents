from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from autogen_core.models import ChatCompletionClient
import os

AGENT_NAME = "FileListener"
AGENT_INSTRUCTIONS = (
    "You are a helpful AI assistant with file system access. "
    "When a user requests a list of files, locate and list all files in the system."
)


async def list_files(path: str) -> str:
    """
    Recursively lists all files in the specified directory, excluding hidden directories.

    Args:
        path (str): The directory path to search.

    Returns:
        str: A newline-separated list of file paths, or an error message if the path is invalid.
    """
    if not os.path.isdir(path):
        return f"Error: '{path}' is not a valid directory."

    file_list = []
    for root, dirs, files in os.walk(path, topdown=True):
        # Exclude directories that start with a dot (hidden directories)
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for file in files:
            file_list.append(os.path.join(root, file))

    return "\n".join(file_list)


list_files_tool = FunctionTool(
    func=list_files,
    description="Lists all files in a given directory, excluding hidden directories.",
    name="file_listener",
)


class FileListenerAgent(AssistantAgent):
    """
    An agent that lists files from the file system when requested.
    """

    def __init__(self, name: str, model_client: ChatCompletionClient):
        super().__init__(
            name=name,
            model_client=model_client,
            description=AGENT_INSTRUCTIONS,
            tools=[list_files_tool],
        )
