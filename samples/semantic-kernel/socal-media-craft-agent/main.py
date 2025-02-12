import asyncio
import os

from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.agents.strategies.termination.termination_strategy import (
    TerminationStrategy,
)
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from agents.seo_boost_agent import SeoBoostAgent
from agents.social_craft_agent import SocialCraftAgent

from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import (
    AzureChatCompletion,
)
from semantic_kernel.kernel import Kernel


class ApprovalTerminationStrategy(TerminationStrategy):
    async def should_agent_terminate(self, agent, history):
        return "approved" in history[-1].content.lower()


async def main():

    kernel = Kernel()
    kernel.add_service(AzureChatCompletion())

    agent_seo = SeoBoostAgent(kernel)
    agent_social = SocialCraftAgent(kernel)

    chat = AgentGroupChat(
        agents=[agent_social, agent_seo],
        termination_strategy=ApprovalTerminationStrategy(
            agents=[agent_seo], maximum_iterations=15
        ),
    )

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "blog.md")

    with open(filename, "r", encoding="utf-8") as file:
        blog_content = file.read().replace("\n", "")

    input = f"Create a social media post for the given blog content '{blog_content}'"
    await chat.add_chat_message(ChatMessageContent(role=AuthorRole.USER, content=input))

    async for content in chat.invoke():
        print(f"\033[91m{content.name}:\033[0m")
        print(content.content)
        print("_" * os.get_terminal_size().columns)

    print(f"# IS COMPLETE: {chat.is_complete}")


if __name__ == "__main__":
    asyncio.run(main())
