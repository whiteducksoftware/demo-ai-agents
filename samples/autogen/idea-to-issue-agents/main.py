from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from agents.project_idea_agent import ProjectIdeaAgent
from agents.user_story_agent import UserStoryAgent
from agents.github_issue_agent import GitHubIssueAgent
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
github_token = os.getenv("GITHUB_TOKEN")
github_repository = os.getenv("GITHUB_REPOSITORY")


az_model_client = AzureOpenAIChatCompletionClient(
    azure_deployment=azure_deployment,
    model=model,
    api_version=api_version,
    azure_endpoint=azure_endpoint,
    azure_ad_token_provider=token_provider,
)


# AGENTS
user_proxy = UserProxyAgent("user_proxy")
project_idea_agent = ProjectIdeaAgent(az_model_client)
user_story_agent = UserStoryAgent(az_model_client)
github_issue_agent = GitHubIssueAgent(
    az_model_client,
    github_token=github_token,
    github_repository=github_repository,
)

termination = TextMentionTermination("TERMINATE")


async def main() -> None:

    agent_team = SelectorGroupChat(
        [
            project_idea_agent,
            user_proxy,
            user_story_agent,
            github_issue_agent,
        ],
        model_client=az_model_client,
        selector_prompt="""
            You are the cordinator of role play game. The following roles are available:
            {roles}. 
            
            Rules:
            - Given a task, the project_idea_agent will be tasked to create a project idea.
            - After that, use the user_proxy to request feedback from the user and either hand back to the project_idea_agent or proceed to the next role.
            - The user_story_agent will be tasked with creating user stories based on the project idea.
            - The github_issue_agent will be tasked with creating GitHub issues based on the user stories.
            
            Read the following conversation. Then select the next role from {participants} to play. Only return the role.
            {history}
            Read the above conversation. Then select the next role from {participants} to play. Only return the role.

        """,
        max_turns=10,  # safety net
        termination_condition=termination,
    )

    user_input = """
      Create a simple, innovative software idea. 
    """

    stream = agent_team.run_stream(task=user_input)
    await Console(stream)


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
