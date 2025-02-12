from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
import requests

AGENT_NAME = "github_issue_agent"
AGENT_INSTRUCTIONS = """
    You are the GitHub Integration Agent. Your responsibility is to create a GitHub issue for each user story provided. For every user story, perform the following:

    1. Use the user story title as the GitHub issue title.
    2. Construct the issue body to include:
      - The complete user story description.
      - A clearly formatted list of acceptance criteria.
    
    3. Interact with the GitHub API to post the issue to the designated repository using the create_github_issue function.
"""


class GitHubIssueAgent(AssistantAgent):
    """
    An agent that creates user stories based on a given software idea.
    """

    def __init__(
        self,
        model_client: ChatCompletionClient,
        github_repository: str,
        github_token: str,
    ):
        self.github_repository = github_repository
        self.github_token = github_token
        super().__init__(
            name=AGENT_NAME,
            model_client=model_client,
            system_message=AGENT_INSTRUCTIONS,
            tools=[self.create_github_issue],
        )

    def create_github_issue(self, title: str, body: str) -> str:
        url = f"https://api.github.com/repos/{self.github_repository}/issues"
        headers = {
            "Authorization": f"Bearer {self.github_token}",
            "Accept": "application/vnd.github+json",
        }
        issue_title = title
        issue_body = body

        payload = {"title": issue_title, "body": issue_body}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 201:
            return "Issue created successfully."
        else:
            return "Failed to create issue. Please try again later."
