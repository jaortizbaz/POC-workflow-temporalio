import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from etl.activity.api_activities import get_data_from_star_wars_api
from etl.activity.sftp_activities import check_filename
from etl.config.config import Config
from etl.workflows.star_wars_workflow import StarWarsEtl


async def main():
    config = Config()
    client = await Client.connect(config.TEMPORALIO_HOST)
    worker = Worker(
        client,
        task_queue=config.TASK_QUEUE_NAME,
        workflows=[StarWarsEtl],
        activities=[check_filename, get_data_from_star_wars_api],
        activity_executor=ThreadPoolExecutor(5),
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
