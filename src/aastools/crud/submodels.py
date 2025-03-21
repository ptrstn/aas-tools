from typing import Dict, List
from urllib.parse import quote

import requests

from aastools.settings import settings
from aastools.utils import base64_encoded


def get_submodels(host: str = settings.host) -> List[Dict]:
    """
    Returns all Submodels

    GET /submodels
    """
    url = f"{host}/submodels"

    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    submodels = json_response["result"]
    return submodels


def get_submodel(submodel_id: str, encode=True, host: str = settings.host) -> Dict:
    """
    Returns a specific Submodel

    GET /submodels/{submodel_id}
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}"

    response = requests.get(url)
    response.raise_for_status()
    submodel = response.json()
    return submodel


def delete_submodel(submodel_id: str, encode=True, host: str = settings.host):
    """
    Deletes a specific Submodel

    DELETE /submodels/{submodel_id}
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}"

    response = requests.delete(url)
    response.raise_for_status()


# ─────────────────────────── Submodel elements ───────────────────────────


def get_submodel_elements(submodel_id: str, encode=True, host: str = settings.host):
    """
    Returns all submodel elements of a specific Submodel

    GET /submodels/{submodel_id}/submodel-elements
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}/submodel-elements"

    response = requests.get(url)
    response.raise_for_status()
    json_response = response.json()
    elements = json_response["result"]
    return elements


def get_submodel_element(
    submodel_id: str, id_short_path: str, encode=True, host: str = settings.host
):
    """
    Returns all submodel elements including their hierarchy

    GET /submodels/{submodel_id}/submodel-elements/{id_short_path}
    """
    submodel_id = base64_encoded(submodel_id, encode)
    url = f"{host}/submodels/{submodel_id}/submodel-elements/{id_short_path}"

    response = requests.get(url)
    response.raise_for_status()
    element = response.json()
    return element


def set_submodel_element_value(
    submodel_id: str,
    id_short_path: str,
    value: str,
    encode=True,
    host: str = settings.host,
):
    """
    Updates the value of an existing Submodel Element

    PATCH /submodels/{submodel_id}/submodel-elements/{id_short_path}/$value
    """
    submodel_id = base64_encoded(submodel_id, encode)
    id_short_path = quote(id_short_path)
    url = f"{host}/submodels/{submodel_id}" f"/submodel-elements/{id_short_path}/$value"

    response = requests.patch(url, json=value)
    response.raise_for_status()


def delete_submodel_element(
    submodel_id: str,
    id_short_path: str,
    value: str,
    encode=True,
    host: str = settings.host,
):
    """
    Deletes a submodel element at a specified path

    DELETE /submodels/{submodel_id}/submodel-elements/{idShortPath}
    """
    submodel_id = base64_encoded(submodel_id, encode)
    id_short_path = quote(id_short_path)

    url = f"{host}/submodels/{submodel_id}" f"/submodel-elements/{id_short_path}/$value"
    response = requests.delete(url, json=value)
    response.raise_for_status()
