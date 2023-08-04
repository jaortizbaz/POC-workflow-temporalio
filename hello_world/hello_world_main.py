import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from hello_world.workflow.greeting_workflow import GreetingWorkflow
from hello_world.activity.compose_greeting_activity import compose_greeting


async def main():
    logging.basicConfig(level=logging.INFO)

    client = await Client.connect(target_host="localhost:7233", namespace="hello_world")

    async with Worker(
        client,
        task_queue="hello-activity-task-queue",
        workflows=[GreetingWorkflow],
        activities=[compose_greeting],
        activity_executor=ThreadPoolExecutor(5),
    ):
        result = await client.execute_workflow(
            GreetingWorkflow.run,
            "Woooooooorld",
            id="hello-activity-workflow-id",
            task_queue="hello-activity-task-queue",
        )
        logging.log(logging.INFO, f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
