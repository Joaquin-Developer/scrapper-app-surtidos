import os
from typing import List, Dict, Tuple, Any

import requests

# TODO mejorar la config y diferenciar env test/prod
API_URL = "http://localhost:8081"


def get_credentials() -> Tuple[str, str]:
    user = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")
    return user, password


def get_api_token() -> str:
    url = f"{API_URL}/auth/login"
    username, password = get_credentials()
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, json=payload, headers=headers)
    return response.text


def send_data_to_backend(products: List[Dict[str, Any]]):
    url = f"{API_URL}/api/products/batch"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_api_token()}"
    }

    req = requests.post(url=url, json=products, headers=headers)

    if req.status_code not in (200, 201):
        raise Exception(f"error send_data_to_backend, {str(req.content)}")
