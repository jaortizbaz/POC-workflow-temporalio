import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker, SharedStateManager

from etl.activity.sftp_activities import check_filename
from etl.workflows.star_wars_workflow import StarWarsEtl


async def main():
    client = await Client.connect("localhost:7233")

    async with Worker(
        client,
        task_queue="star_wars_etl",
        activities=[check_filename],
        workflows=[StarWarsEtl],
        # Synchronous activities are not allowed unless we provide some kind of
        # executor. Here we are giving a process pool executor which means the
        # activity will actually run in a separate process. This same executor
        # could be passed to multiple workers if desired.
        activity_executor=ProcessPoolExecutor(5),
        # Since we are using an executor that is not a thread pool executor,
        # Temporal needs some kind of manager to share state such as
        # cancellation info and heartbeat info between the host and the
        # activity. Therefore, we must provide a shared_state_manager here. A
        # helper is provided to create it from a multiprocessing manager.
        shared_state_manager=SharedStateManager.create_from_multiprocessing(
            multiprocessing.Manager()
        ),
    ):
        result = await client.execute_workflow(
            StarWarsEtl.run,
            "file_star_wars.csv",
            id="poc-hello-world-wf",
            task_queue="say_hello_task_queue",
        )

        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
