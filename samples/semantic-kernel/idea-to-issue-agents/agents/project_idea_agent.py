from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.kernel import Kernel

AGENT_NAME = "project_idea_agent"
AGENT_INSTRUCTIONS = """
You are the Software Idea Generator Agent. 
Generate a simple, innovative software idea in one concise sentence (e.g., "A collaborative, minimalist todo list app."). Keep it brief and avoid complexity.
"""


class ProjectIdeaAgent(ChatCompletionAgent):
    """
    An agent that creates a software project idea.
    """

    def __init__(self, name: str, kernel: Kernel):
        super().__init__(
            service_id=name, name=name, kernel=kernel, instructions=AGENT_INSTRUCTIONS
        )
