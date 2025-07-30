import requests

def shared_pages(headers, query=None):
    endpoint = "https://api.notion.com/v1/search"
    payload = {
        "filter": {"property": "object", "value": "page"}
        }
    
    if query:
        payload["query"] = query    
    
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()  # Raises an error for bad responses
    return response.json()
    