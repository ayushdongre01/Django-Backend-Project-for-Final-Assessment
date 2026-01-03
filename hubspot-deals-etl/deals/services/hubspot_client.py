import requests
from django.conf import settings

BASE_URL = "https://api.hubapi.com"

HEADERS = {
    "Authorization": f"Bearer {settings.HUBSPOT_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def fetch_deals(limit=50, after=None):
    params = {"limit": limit}
    if after:
        params["after"] = after

    response = requests.get(
        f"{BASE_URL}/crm/v3/objects/deals",
        headers=HEADERS,
        params=params,
        timeout=30
    )
    response.raise_for_status()
    return response.json()
