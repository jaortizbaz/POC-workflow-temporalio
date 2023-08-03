from temporalio import activity
from sftp_api_process.repository.star_wars_api import get_person_by_id, get_resource_by_url


@activity.defn
async def get_person_data_from_star_wars_api(person_id: int) -> dict:
    activity.logger.info(f"Running activity to get person data for {person_id}")
    try:
        person = await get_person_by_id(person_id)
        return person
    except Exception as e:
        activity.logger.error(f"Error getting person data from API for ID {person_id}. Cause: {e}")


@activity.defn
async def get_planet_data_from_star_wars_api(planet_url: str) -> dict:
    activity.logger.info(f"Running activity to get planet data for {planet_url}")
    try:
        planet = await get_resource_by_url(planet_url)
        return planet
    except Exception as e:
        activity.logger.error(f"Error getting person data from API for ID {planet_url}. Cause: {e}")
