import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from greeting_workflow import GreetingWorkflow
from compose_greeting_activity import compose_greeting


async def main():
    logging.basicConfig(level=logging.INFO)

    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[GreetingWorkflow],
        activities=[compose_greeting],
    ):
        result = await client.execute_workflow(
            GreetingWorkflow.run,
            "World",
            id="hello-activity-workflow-id",
            task_queue="hello-activity-task-queue",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
