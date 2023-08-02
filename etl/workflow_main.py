import asyncio
from typing import Optional

from temporalio.client import Client, WorkflowFailureError
from temporalio.exceptions import FailureError
from etl.config.config import Config
from etl.entity.sftp_properties import SftpProps
from etl.workflows.star_wars_workflow import StarWarsEtl


async def main():
    config = Config()
    client = await Client.connect(config.TEMPORALIO_HOST)
    try:
        for workflow_id in config.WORKFLOW_IDS:
            handle = await client.start_workflow(
                workflow=StarWarsEtl.run,
                arg=SftpProps(config.SFTP_FILEPATTERN),
                id=workflow_id,
                task_queue=config.TASK_QUEUE_NAME,
                cron_schedule="* * * * *",
            )

            result = await handle.result()

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
