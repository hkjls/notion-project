import requests

def get_notion_response(notion_key):
    endpoint = "https://api.notion.com/v1/pages"
    response = requests.get(endpoint)
                            #  headers={
                            #      "Authorization": f"Bearer {notion_key}",
                            #      "notion-version": "2022-06-28",
                            #      "Content-Type": "application/json"
                            # })
    
    print(response.status_code)
    
    if response.status_code == 200:
        return response.json()