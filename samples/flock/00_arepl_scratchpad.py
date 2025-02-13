import asyncio
from dataclasses import dataclass
from flock.core.tools import basic_tools
from flock.core.logging.formatters.base_formatter import FormatterOptions
from flock.core.logging.formatters.rich_formatters import RichTables

from flock.core import Flock, FlockAgent


MODEL = "openai/gpt-4o"

@dataclass
class MyBlog:
    title: str
    fitting_emoji: str
    sub_headers: list
    blog_summary: str

format_options = FormatterOptions(RichTables)
flock = Flock(local_debug=True, output_formatter=format_options)

bloggy = FlockAgent(name="bloggy", input="blog_idea",
                    output="blog: MyBlog")

flock.add_agent(bloggy)

agent = FlockAgent(
        name="my_agent",
        input="url",
        output="title, headings: list[str], entities_and_metadata: list[dict[str, str]], type:Literal['news', 'blog', 'opinion piece', 'tweet']",
        tools=[basic_tools.get_web_content_as_markdown],
        use_cache=True,
    )
flock.add_agent(agent)

asyncio.run(flock.run_async(
        start_agent=agent,
        input={"url": "https://lite.cnn.com/travel/alexander-the-great-macedon-persian-empire-darius/index.html"},
    ))