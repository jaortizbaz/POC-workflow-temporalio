from temporalio import activity
from etl.repository.star_wars_api import get_person_by_id


@activity.defn
async def get_data_from_star_wars_api(person_id: int) -> dict:
    activity.logger.info(f"Running activity to wait for file {person_id}")
    try:
        result = {}
        person = await get_person_by_id(person_id)
        result['person'] = person
        return result
    except Exception as e:
        activity.logger.error(f"Error getting information from API for ID {person_id}. Cause: {e}")
