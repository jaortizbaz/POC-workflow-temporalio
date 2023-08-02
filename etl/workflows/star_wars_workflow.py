from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from etl.activity.api_activities import get_data_from_star_wars_api
from etl.activity.sftp_activities import check_filename
from etl.entity.sftp_properties import SftpProps


@workflow.defn
class StarWarsWorkflow:
    def __init__(self):
        self._has_file = None
        self._star_wars_details = None

    @workflow.run
    async def run(self):
        await workflow.wait_condition(lambda: self._has_file is not None)

        if self._has_file:
            star_wars_data = await workflow.execute_activity(
                activity=get_data_from_star_wars_api,
                arg=1,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(maximum_attempts=3)
            )

            self._star_wars_details = star_wars_data

    @workflow.signal
    async def set_has_file(self, has_file):
        self._has_file = has_file

    @workflow.query
    async def get_star_wars_details(self):
        return self._star_wars_details
