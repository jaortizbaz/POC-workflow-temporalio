from temporalio import activity
from dataclasses import dataclass


@dataclass
class ComposeGreetingInput:
    greeting: str
    name: str


@activity.defn
async def compose_greeting(greeting_input: ComposeGreetingInput) -> str:
    activity.logger.info("Running activity with parameter %s" % greeting_input)
    return f"{greeting_input.greeting}, {greeting_input.name}!"
