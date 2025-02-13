import asyncio
from dataclasses import dataclass

from flock.core import Flock, FlockAgent


@dataclass
class MyCoolBlog:
    funny_blog_title: str
    blog_headers: list
    fitting_emoji: str
    extra_ordinary_ideas: list[str]
    blog_summary: str


flock = Flock(local_debug=True)

bloggy = FlockAgent(name="Bloggy", input="blog_idea", output="mycoolblog: MyCoolBlog")

flock.add_agent(bloggy)

result = asyncio.run(
    flock.run_async(start_agent=bloggy, input={"blog_idea": "Rosenheim"})
)
