from sftp_api_process.config.config import Config


PEOPLE = 'people'


async def __get_api_data(url: str) -> dict:
    print(f"Getting data from {url}")
    import requests
    response = requests.get(url=url)
    response.raise_for_status()
    json_result = response.json()
    print(f"received data: {json_result}")
    return json_result


async def __get_resource(resource: str, resource_id: int | None = None) -> dict:
    config = Config()
    url = f'{config.API_BASE_URL}{resource}/{resource_id if resource_id else ""}'
    result = await __get_api_data(url)
    return result


async def get_resource_by_url(url: str):
    result = await __get_api_data(url)
    return result


async def get_person_by_id(person_id: int | None = None) -> dict:
    result = await __get_resource(PEOPLE, person_id)
    return result



