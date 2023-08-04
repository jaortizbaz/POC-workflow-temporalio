import time
import uuid

from temporalio import activity
from temporalio.client import Client, WorkflowExecutionStatus
from temporalio.worker import Worker

from sftp_api_process.entity.sftp_properties import SftpProps
from sftp_api_process.workflows.sftp_workflow import SftpWorkflow, SftpWorkflowProps
from sftp_api_process.workflows.star_wars_workflow import StarWarsWorkflow


@activity.defn(name="check_filename")
async def check_filename_mocked(input_data: SftpProps) -> bool:
    return True


@activity.defn(name="get_person_data_from_star_wars_api")
async def get_person_data_from_star_wars_api_mock(person_id: int):
    return {"id": person_id, "homeworld": "some_url"}


@activity.defn(name="get_planet_data_from_star_wars_api")
async def get_planet_data_from_star_wars_api_mock(planet_url: str):
    return {"id": 1}


async def test_workflow_for_odd_person_id(client: Client):
    task_queue_name = str(uuid.uuid4())
    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[SftpWorkflow, StarWarsWorkflow],
        activities=[check_filename_mocked, get_person_data_from_star_wars_api_mock,
                    get_planet_data_from_star_wars_api_mock]
    ):
        await client.start_workflow(
            workflow=SftpWorkflow.run,
            arg=SftpWorkflowProps(SftpProps("some_filename"), "some_id"),
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )
        star_wars_handle = await client.start_workflow(
            workflow=StarWarsWorkflow.run,
            arg=1,
            id="some_id",
            task_queue=task_queue_name,
        )

        assert WorkflowExecutionStatus.RUNNING == (await star_wars_handle.describe()).status

        while (await star_wars_handle.describe()).status == WorkflowExecutionStatus.RUNNING:
            time.sleep(1)

        assert WorkflowExecutionStatus.COMPLETED == (await star_wars_handle.describe()).status

        star_wars_has_file = await star_wars_handle.query(StarWarsWorkflow.has_file)
        star_wars_result = await star_wars_handle.query(StarWarsWorkflow.get_star_wars_details)

        assert star_wars_has_file is True
        assert star_wars_result["person"]["id"] == 1
        assert star_wars_result["planet"] is None


async def test_workflow_for_even_person_id(client: Client):
    task_queue_name = str(uuid.uuid4())
    async with Worker(
        client,
        task_queue=task_queue_name,
        workflows=[SftpWorkflow, StarWarsWorkflow],
        activities=[check_filename_mocked, get_person_data_from_star_wars_api_mock,
                    get_planet_data_from_star_wars_api_mock]
    ):
        await client.start_workflow(
            workflow=SftpWorkflow.run,
            arg=SftpWorkflowProps(SftpProps("some_filename"), "some_id"),
            id=str(uuid.uuid4()),
            task_queue=task_queue_name,
        )
        star_wars_handle = await client.start_workflow(
            workflow=StarWarsWorkflow.run,
            arg=2,
            id="some_id",
            task_queue=task_queue_name,
        )

        while (await star_wars_handle.describe()).status == WorkflowExecutionStatus.RUNNING:
            time.sleep(1)

        star_wars_result = await star_wars_handle.query(StarWarsWorkflow.get_star_wars_details)

        assert star_wars_result["person"]["id"] == 2
        assert star_wars_result["planet"]["id"] == 1
