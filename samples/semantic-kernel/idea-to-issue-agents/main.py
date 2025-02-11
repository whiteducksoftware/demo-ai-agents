import asyncio
import os

from semantic_kernel.kernel import Kernel
from semantic_kernel.agents import AgentGroupChat
from semantic_kernel.agents.strategies.termination.termination_strategy import (
    TerminationStrategy,
)
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from agents.project_idea_agent import ProjectIdeaAgent
from agents.user_story_agent import UserStoryAgent
from agents.github_issue_agent import GitHubIssueAgent


class ApprovalTerminationStrategy(TerminationStrategy):
    async def should_agent_terminate(self, agent, history):
        return "approved" in history[-1].content.lower()


async def main():
    kernel = Kernel()

    agent_idea = ProjectIdeaAgent(name="project_idea_agent", kernel=kernel)
    agent_story = UserStoryAgent(name="user_story_agent", kernel=kernel)
    agent_github = GitHubIssueAgent(
        name="github_issue_agent",
        kernel=kernel,
        github_repository="your-repo",
        github_token="your-token",
    )

    chat = AgentGroupChat(
        agents=[agent_idea, agent_story, agent_github],
        termination_strategy=ApprovalTerminationStrategy(
            agents=[agent_idea], maximum_iterations=15
        ),
    )

    with open("blog.md", "r", encoding="utf-8") as file:
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
