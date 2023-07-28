from datetime import timedelta

from temporalio import workflow
from hello_world.activity.compose_greeting_activity import (
    ComposeGreetingInput,
    compose_greeting,
)


@workflow.defn
class GreetingWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        workflow.logger.info("Running workflow with parameter %s" % name)
        result = await workflow.execute_activity(
            compose_greeting,
            ComposeGreetingInput("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )
        return result
