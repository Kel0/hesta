from typing import Union

import requests


async def get_commits_of_repository(
    profile_link: str, repository_name: str
) -> Union[dict, list]:
    """
    Get commits of repository
    :return json_data: Dict
    """
    profile_name: str = profile_link.split("/")[-1]

    response: requests.Response = requests.get(
        url=f"https://api.github.com/repos/{profile_name}/{repository_name}/commits"
    )
    json_data = response.json()
    return json_data
