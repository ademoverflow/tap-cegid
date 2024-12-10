"""This module contains the function to authenticate with the Cegid API."""

from __future__ import annotations

import requests


def get_token(username: str, password: str) -> dict | None:
    """Get the token from the Cegid API."""
    url = "https://retail-services.cegid.cloud/t/as/connect/token"

    # Define the form data
    data = {
        "client_id": "CegidRetailResourceFlowClient",
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "RetailBackendApi offline_access",
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None
