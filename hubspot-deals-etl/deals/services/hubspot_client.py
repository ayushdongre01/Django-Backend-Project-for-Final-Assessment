import os
import requests

HUBSPOT_BASE_URL = "https://api.hubapi.com"
ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")

def fetch_deals(after=None, limit=50):
    url = f"{HUBSPOT_BASE_URL}/crm/v3/objects/deals"

    params = {
        "limit": limit,
        "archived": "false",
        "properties": "dealname,dealstage,pipeline,amount,closedate",
    }

    if after:
        params["after"] = after

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        # ❌ DO NOT set Content-Type for GET
    }

    response = requests.get(url, headers=headers, params=params)

    # Temporary debug (VERY IMPORTANT)
    if response.status_code != 200:
        print("HubSpot error:", response.text)

    response.raise_for_status()
    return response.json()
