from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from etl.activity.sftp_activities import check_filename
from etl.entity.sftp_properties import SftpProps


@workflow.defn
class StarWarsEtl:
    @workflow.run
    async def run(self, sftp_props: SftpProps) -> bool:
        file_received = await workflow.execute_activity(
            activity=check_filename,
            arg=sftp_props,
            start_to_close_timeout=timedelta(seconds=10),
            heartbeat_timeout=timedelta(seconds=5),
            retry_policy=RetryPolicy(maximum_attempts=3)
        )

        return file_received
