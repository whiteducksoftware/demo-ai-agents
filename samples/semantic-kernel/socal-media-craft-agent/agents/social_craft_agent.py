from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.kernel import Kernel

AGENT_NAME = "SocialCraftAgent"
AGENT_INSTRUCTIONS = """
You are a social media expert with a talent for creating compelling, clickable posts that capture attention and drive engagement.
Your goal is to generate a single, optimized social media post that summarizes content effectively while maximizing reader interaction. 
Each post should be clear, creative, and impactful. 
Avoid unnecessary details or explanations. 
Refine the post based on any suggestions provided.
"""


class SocialCraftAgent(ChatCompletionAgent):

    def __init__(
        self,
        kernel: Kernel,
    ):
        super().__init__(
            service_id=AGENT_NAME,
            kernel=kernel,
            name=AGENT_NAME,
            instructions=AGENT_INSTRUCTIONS,
        )
