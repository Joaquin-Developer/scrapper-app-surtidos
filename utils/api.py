from typing import List, Dict, Any

import requests

from config import config


def get_api_token() -> str:
    url = f"{config.API_URL}/auth/login"
    payload = {"username": config.API_USERNAME, "password": config.API_PASSWORD}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, json=payload, headers=headers)
    return response.text


def send_data_to_backend(products: List[Dict[str, Any]]):
    url = f"{config.API_URL}/api/products/batch"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_api_token()}"
    }

    req = requests.post(url=url, json=products, headers=headers)

    if req.status_code not in (200, 201):
        raise Exception(f"error send_data_to_backend, {str(req.content)}")
