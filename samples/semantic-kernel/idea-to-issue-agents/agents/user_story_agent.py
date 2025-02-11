from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.kernel import Kernel


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


class UserStoryAgent(ChatCompletionAgent):
    """
    An agent that creates user stories based on a given software idea.
    """

    def __init__(self, name: str, kernel: Kernel):
        super().__init__(
            service_id=name, name=name, kernel=kernel, instructions=AGENT_INSTRUCTIONS
        )
