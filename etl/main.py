import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from etl.activity.sftp_activities import check_filename
from etl.config.config import Config
from etl.entity.sftp_properties import SftpProps
from etl.workflows.star_wars_workflow import StarWarsEtl


TASK_QUEUE_NAME = "star_wars_task_etl"
WORKFLOW_ID = "poc-star-wars-wf"


async def main():
    config = Config()
    client = await Client.connect(config.TEMPORALIO_HOST)

    async with Worker(
        client=client,
        task_queue=TASK_QUEUE_NAME,
        activities=[check_filename],
        workflows=[StarWarsEtl],
        activity_executor=ThreadPoolExecutor(5),
    ):
        result = await client.execute_workflow(
            workflow=StarWarsEtl.run,
            arg=SftpProps(config.SFTP_HOST,
                          config.SFTP_PORT,
                          config.SFTP_USER,
                          config.SFTP_PASSWORD,
                          config.SFTP_PATH,
                          config.SFTP_FILEPATTERN,
                          ),
            id=WORKFLOW_ID,
            task_queue=TASK_QUEUE_NAME,
        )

        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
