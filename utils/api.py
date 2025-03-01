from typing import List, Dict, Any

import requests

# TODO mejorar la config y diferenciar env test/prod
API_URL = "http://localhost:8081"


def send_data_to_backend(products: List[Dict[str, Any]]):
    url = f"{API_URL}/api/products/batch"
    headers = {"Content-Type": "application/json"}

    req = requests.post(url=url, json=products, headers=headers)

    if req.status_code not in (200, 201):
        raise Exception(f"error send_data_to_backend, {str(req.content)}")
