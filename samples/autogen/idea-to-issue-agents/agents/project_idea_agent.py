from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient

AGENT_NAME = "project_idea_agent"
AGENT_INSTRUCTIONS = """
You are the Software Idea Generator Agent. 
Generate a simple, innovative software idea in one concise sentence (e.g., "A collaborative, minimalist todo list app."). Keep it brief and avoid complexity.
"""


class ProjectIdeaAgent(AssistantAgent):
    """
    An agent that creates a software project idea.
    """

    def __init__(self, model_client: ChatCompletionClient):
        super().__init__(
            name=AGENT_NAME,
            model_client=model_client,
            system_message=AGENT_INSTRUCTIONS,
        )
