from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.kernel import Kernel

AGENT_NAME = "SeoBoostAgent"
AGENT_INSTRUCTIONS = """
You are an SEO optimizer with deep expertise in search engine algorithms and a focus on driving organic traffic. 
Your goal is to evaluate whether the provided content is optimized for SEO best practices. 
If the content meets standards, confirm that it is approved. ALWAYS use the word "approved" in that case.
If not, provide insights on how to improve SEO factors, without giving specific examples in a SINGLE proposal per respond. Focus on one point at a time. Keep it short!.
"""


class SeoBoostAgent(ChatCompletionAgent):

    def __init__(self, kernel: Kernel):
        super().__init__(
            service_id=AGENT_NAME,
            kernel=kernel,
            name=AGENT_NAME,
            instructions=AGENT_INSTRUCTIONS,
        )
