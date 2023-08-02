import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from temporalio.client import Client, WorkflowFailureError
from temporalio.exceptions import FailureError
from temporalio.worker import Worker

from etl.activity.api_activities import get_data_from_star_wars_api
from etl.activity.sftp_activities import check_filename
from etl.config.config import Config
from etl.entity.sftp_properties import SftpProps
from etl.workflows.star_wars_workflow import StarWarsEtl


TASK_QUEUE_NAME = "star_wars_task_etl"
WORKFLOW_IDS = ["poc-star-wars-wf"]


async def main():
    config = Config()
    client = await Client.connect(config.TEMPORALIO_HOST)

    async with Worker(
        client=client,
        task_queue=TASK_QUEUE_NAME,
        activities=[check_filename, get_data_from_star_wars_api],
        workflows=[StarWarsEtl],
        activity_executor=ThreadPoolExecutor(5),
    ):
        try:
            for workflow_id in WORKFLOW_IDS:
                result = await client.execute_workflow(
                    workflow=StarWarsEtl.run,
                    arg=SftpProps(config.SFTP_HOST,
                                  config.SFTP_PORT,
                                  config.SFTP_USER,
                                  config.SFTP_PASSWORD,
                                  config.SFTP_PATH,
                                  config.SFTP_FILEPATTERN,
                                  ),
                    id=workflow_id,
                    task_queue=TASK_QUEUE_NAME,
                    cron_schedule="* * * * *",
                )

                print(f"Result: {result}")
        except WorkflowFailureError as e:
            append_temporal_stack(e)


def append_temporal_stack(exc: Optional[BaseException]) -> None:
    while exc:
        if (
            isinstance(exc, FailureError)
            and exc.failure
            and exc.failure.stack_trace
            and len(exc.args) == 1
            and "\nStack:\n" not in exc.args[0]
        ):
            exc.args = (f"{exc}\nStack:\n{exc.failure.stack_trace.rstrip()}",)
        exc = exc.__cause__


if __name__ == "__main__":
    asyncio.run(main())
