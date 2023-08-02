from dataclasses import dataclass
from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy

from etl.activity.sftp_activities import check_filename
from etl.entity.sftp_properties import SftpProps
from etl.workflows.star_wars_workflow import StarWarsWorkflow


@dataclass
class SftpWorkflowProps:
    sftp_props: SftpProps
    workflow_id: str


@workflow.defn
class SftpWorkflow:
    @workflow.run
    async def run(self, sftp_workflow_props: SftpWorkflowProps):
        file_received = await workflow.execute_activity(
            activity=check_filename,
            arg=sftp_workflow_props.sftp_props,
            start_to_close_timeout=timedelta(seconds=10),
            heartbeat_timeout=timedelta(seconds=5),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )

        if not file_received:
            raise RuntimeError(f"File {sftp_workflow_props.sftp_props.filename} not received.")

        handle = workflow.get_external_workflow_handle_for(StarWarsWorkflow.run,
                                                           workflow_id=sftp_workflow_props.workflow_id)
        await handle.signal(StarWarsWorkflow.set_has_file, file_received)
