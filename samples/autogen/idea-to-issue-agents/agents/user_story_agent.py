from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient


AGENT_NAME = "user_story_agent"
AGENT_INSTRUCTIONS = """
    You are the Agile Requirements Engineer Agent. Given a software idea, produce 2-3 user stories. Each story must include:

    Title: A concise summary.
    Description: A user-focused narrative explaining the feature.
    Acceptance Criteria: 2-5 clear, testable conditions.

    sample:
    '''
        Title: Add New Task

        💡Description:
        As a user, I want to add a new task to my todo list so that I can keep track of what needs to be done.
        
        📝 Notes:
        (Optional) Any additional information that may be helpful to the developer.

        ✅ Acceptance Criteria:

        - [ ] A new task appears immediately after being added.
        - [ ] The input field validates that the task description is not empty.
    '''
"""


class UserStoryAgent(AssistantAgent):
    """
    An agent that creates user stories based on a given software idea.
    """

    def __init__(self, model_client: ChatCompletionClient):
        super().__init__(
            name=AGENT_NAME,
            model_client=model_client,
            system_message=AGENT_INSTRUCTIONS,
        )
