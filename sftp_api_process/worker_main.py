import asyncio
from concurrent.futures import ThreadPoolExecutor

from temporalio.client import Client
from temporalio.worker import Worker

from sftp_api_process.activity.api_activities import get_person_data_from_star_wars_api
from sftp_api_process.activity.sftp_activities import check_filename
from sftp_api_process.config.config import Config
from sftp_api_process.workflows.sftp_workflow import SftpWorkflow
from sftp_api_process.workflows.star_wars_workflow import StarWarsWorkflow


async def main():
    config = Config()
    client = await Client.connect(config.TEMPORALIO_HOST)
    worker = Worker(
        client,
        task_queue=config.TASK_QUEUE_NAME,
        workflows=[StarWarsWorkflow, SftpWorkflow],
        activities=[check_filename, get_person_data_from_star_wars_api],
        activity_executor=ThreadPoolExecutor(5),
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
