from notion_client import AsyncClient, Client
from pprint import pprint
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime

load_dotenv()

payload = {
    "filter": {"property": "object", "value": "database"},
}

def user_list():
    # notion = AsyncClient(auth=os.getenv('notion_key'))
    notion = Client(auth=os.getenv('notion_key'))
    all_results = []
    response = notion.search(
        start_cursor=None,
        **payload
    )
    
    all_results.extend(response['results'])
    
    dbs_title = list(map(lambda x: x['title'][0]['text']['content'], all_results))
    dbs_id = list(map(lambda x: x['id'], all_results))
    
    dbs = zip(dbs_title, dbs_id)
    dbs = list(dbs)
    next_cursor = None
    has_more = True
    
    while has_more:
        db = notion.databases.query(
            database_id=list(filter(lambda x:x[0]=="List", dbs))[0][1],
            start_cursor=next_cursor,
            page_size=100,
            filter={
                "property":"Date",
                "date":{
                    "on_or_before": datetime.now().isoformat(),
                }
            },
            sorts=[
                {
                    "property": "Date",
                    "direction": "descending"
                }]
        )
        
        has_more = db.get("has_more")
        next_cursor = db.get("next_cursor")
        
        pages_propreties = list(map(lambda x: x['properties'], db['results']))
        columns = list(map(lambda x:dict(x).keys(), pages_propreties))[0]
        # print(columns)
        project_value = list(map(lambda x:list(x.values()), pages_propreties))
        
        project_value = list(map(lambda x:{"status":x[0], "title":x[-1]}, project_value))
        project_title = list(filter(lambda x:len(x['title']['title']) > 0, project_value))
        
        project_list = list(map(lambda x:{'status':x['status'][x['status']['type']], 'title':x['title']['title'][0]['text']['content']}, project_title))
        finished = list(filter(lambda x:x['status']==True, project_list))
        print(finished)
        # project_title = list(map(lambda x:x['title'][0]['text']['content'], project_title))

        # print(project_title)
        # print("..................")
    return response
    
    
    
if __name__ == "__main__":
    # asyncio.run(user_list())
    user_list()