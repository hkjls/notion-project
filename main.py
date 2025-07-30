from dotenv import load_dotenv
import os

from modules.notionRequest import get_notion_response
from modules.get_shared_pages import shared_pages

load_dotenv()

headers = {
    "Authorization": f"Bearer {os.getenv('notion_key')}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}


def main():
    print("Welcome into the Notion Integration Module!")
    notion_response = shared_pages(headers)
    
    pages_details = notion_response["results"]
    page = list(filter(lambda x:x['parent']['type'] == "page_id", pages_details))
    block = list(filter(lambda x:x['parent']['type'] == "block_id", pages_details))
    workspaces = list(filter(lambda x:x['parent']['type'] == "workspace", pages_details))
    database = list(filter(lambda x:x['parent']['type'] == "database_id", pages_details))
    
    technic_list = list(map(lambda x:x["properties"], database))
    
    # print(technic_list)
    type_list = list(map(lambda x:x['parent']["type"], pages_details))
    print(list(set(type_list)))
    
    # print(database[0]["properties"]["Technic"]["title"][0]["text"]["content"])
    print("Content Number:",len(workspaces))
    print(list(map(lambda x:x['properties'], workspaces)))
    print("-----------------------------")
    
    print("Content Number:",len(page))
    print(list(map(lambda x:x['properties'], page)))
    print("-----------------------------")
    
    print("Content Number:",len(block))
    print(list(map(lambda x:x['properties'], block)))
    print("-----------------------------")
    
    print("Content Number:",len(database))
    print(list(map(lambda x:x['properties'], database)))
if __name__ == "__main__":
    main()