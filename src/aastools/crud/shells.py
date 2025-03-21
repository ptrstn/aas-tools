from typing import Dict, List

import requests

from aastools.settings import settings
from aastools.utils import base64_encoded


def get_shells(host: str = settings.host) -> List[Dict]:
    url = f"{host}/shells"
    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    shells = json_response["result"]
    return shells


def get_shell(shell_id, encode=True, host: str = settings.host) -> Dict:
    shell_id = base64_encoded(shell_id, encode)
    url = f"{host}/shells/{shell_id}"

    response = requests.get(url)
    response.raise_for_status()
    shell = response.json()
    return shell


def delete_shell(shell_id: str, encode=True, host: str = settings.host):
    shell_id = base64_encoded(shell_id, encode)

    url = f"{host}/shells/{shell_id}"
    response = requests.delete(url)
    response.raise_for_status()


def delete_submodel_ref(
    shell_id: str,
    submodel_id,
    encode=True,
    host: str = settings.host,
):
    shell_id = base64_encoded(shell_id, encode)
    submodel_id = base64_encoded(submodel_id, encode)

    url = f"{host}/shells/{shell_id}/submodel-refs/{submodel_id}"
    response = requests.delete(url)
    response.raise_for_status()
