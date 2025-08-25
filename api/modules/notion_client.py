from notion_client import Client
import os
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from .notionExtract import save_task_from_json

load_dotenv(Path(__file__).resolve().parent.parent.parent/'.env')

notion = Client(auth=os.getenv('notion_key'))

def get_db(db_name):
    try:
        # Recherche de la base de données
        search_result = notion.search(
            filter={"property": "object", "value": "database"}
        )

        # Trouver la base de données correspondante
        db_id = next(
            (item['id'] for item in search_result['results'] 
             if item['title'][0]['text']['content'] == db_name),
            None
        )

        if not db_id:
            return {"error": "Database not found", "status": 404}

        # Récupérer le contenu de la base de données
        db_content = notion.databases.query(
            database_id=db_id,
            start_cursor=None,
            page_size=10,
            # Tri par date décroissante
            sorts=[{"property": "Date", "direction": "descending"}],
            filter={
                "property": "Projects",
                "relation":{"is_not_empty":True}
                }
        )
        # columns = db_content['results'][0]['properties']
        # print(columns)
        next_cursor = db_content['next_cursor']
        has_more = db_content["has_more"]
        # Simplifier la réponse
        data = {
            "data": [{
                "id": page['id'],
                "properties": {
                    key: value.get('rich_text', [{}])[0].get('text', {}).get('content', '')
                    if value.get('type') == 'rich_text'
                    else value.get('title', [{}])[0].get('text', {}).get('content', '')
                    if value.get('type') == 'title'
                    else value.get('date', {}).get('start', '')
                    if value.get('type') == 'date'
                    else value.get('checkbox', False)
                    if value.get('type') == 'checkbox'
                    else value.get('select', {}).get('name', '')
                    if value.get('type') == 'select'
                    else ''
                    for key, value in page['properties'].items()
                }
            } for page in db_content['results']]
        }
        # Sauvegarder chaque tâche
        saved_count = 0
        for item in data['data']:
            props = item['properties']
            task_data = {
                'tasks': props.get('Tasks', ''),
                'date': props.get('Date', datetime.now().date().isoformat()),
                'projects': props.get('Projects', ''),
                'done': props.get('Done', False),
                'clients': props.get('Clients', ''),
                'entreprise': props.get('Company', ''),
                'tech_stack': props.get('Tech Stack', '')
            }
            try:
                save_task_from_json(task_data)
                saved_count += 1
            except Exception as e:
                print(f"Error saving task: {e}")
                continue
        
        return {"success": 200, "saved_items": saved_count}
    except Exception as e:
        return {"error": str(e), "status": 500}