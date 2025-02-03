from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from agents.file_listener_agent import FileListenerAgent
from agents.file_selector_agent import FileSelectorAgent
from agents.markdown_writer_agent import MarkdownWriterAgent
from agents.file_reader_agent import FileReaderAgent
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)
azure_deployment = os.getenv("AZURE_DEPLOYMENT")
azure_endpoint = os.getenv("AZURE_ENDPOINT")
model = os.getenv("MODEL")
api_version = os.getenv("API_VERSION")

az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=azure_deployment,
    model=model,
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    azure_ad_token_provider=token_provider,
)

file_surfer = FileReaderAgent(
    model_client=az_model_client,
    name="FileReader",
)

file_listener = FileListenerAgent(
    model_client=az_model_client,
    name="FileListener",
)

file_selector = FileSelectorAgent(
    model_client=az_model_client,
    name="FileSelector",
)

user_proxy = UserProxyAgent("user_proxy")
mdown_writer = MarkdownWriterAgent(name="MarkdownWriter", model_client=az_model_client)


async def main() -> None:

    agent_team = SelectorGroupChat(
        [file_listener, file_surfer, mdown_writer, user_proxy, file_selector],
        model_client=az_model_client,
        selector_prompt="""
         You are in a role play game. The following roles are available:
            {roles}.
            Read the following conversation. Then select the next role from {participants} to play. Only return the role.

            {history}

            Read the above conversation. Then select the next role from {participants} to play. Only return the role.
            
            Rules:
                1. Always start with file_listener.
                2. Then file_selector chooses the relevant files.
                3. Next, file_surfer reads the file content.
                4. Then mdown_writer writes markdown.
                5. After mdown_writer, call user_proxy.
                6. Finally, hand back to mdown_writer.  

        """,
    )

    user_input = """
       I want to create a README.md file for a Python project. 
       List all project files and determine which ones are relevant based on their names. 
       Then, use the file_reader tool to read the content of the relevant files. 
       Generate a README.md file with the following sections:
        - Project Description
        - Installation Instructions
        
        Work in the current directory (.).
    """

    stream = agent_team.run_stream(task=user_input)
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
