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
        next_cursor = None
        has_more = True
        # Récupérer le contenu de la base de données
        while has_more:
            db_content = notion.databases.query(
                database_id=db_id,
                start_cursor=next_cursor,
                page_size=20,
                # Tri par date décroissante
                sorts=[{"property": "Date", "direction": "descending"}],
            )
            has_more = db_content["has_more"]
            next_cursor = db_content['next_cursor']

            # Simplifier la réponse
            data = {
                "data": [{
                    "id": page['id'],
                    "properties": {
                        key:value[value['type']]
                        for key, value in page['properties'].items()
                    }
                } for page in db_content['results']]
            }
            
            # Sauvegarder chaque tâche
            saved_count = 0
            entreprise=None
            name=None
            project_name=None
            tech=None
            
            for item in data['data']:
                id=item['id']
                item = item['properties']

                entreprise_array = {
                    'plain_text':""
                }
                name_title={
                    'plain_text':""
                }
                
                projectName = {
                    'plain_text':""
                }
                
                techName = {
                    'plain_text':""
                }
                
                if len(item['Entreprise'][item['Entreprise']['type']])>0:
                    entreprise = item['Entreprise'][item['Entreprise']['type']][0]
                if entreprise is not None:
                    entreprise_array = entreprise[entreprise['type']][0]
                
                if len(item['Name'][item['Name']['type']])>0:
                    name = item['Name'][item['Name']['type']][0]
                if name is not None:
                    name_title = name[name['type']][0]
                    
                if len(item['ProjectsName'][item['ProjectsName']['type']])>0:
                    project_name = item['ProjectsName'][item['ProjectsName']['type']][0]
                if project_name is not None:
                    projectName=project_name[project_name['type']][0]
                    
                if len(item['Techs'][item['Techs']['type']])>0:
                    tech = item['Techs'][item['Techs']['type']][0]
                if tech is not None:
                    techName=tech[tech['type']][0]
                    
                task_data = {
                    'id':id,
                    'done':item['Done'],
                    'projects':projectName['plain_text'],
                    'clients':name_title['plain_text'],
                    'date':item['Date']['start'].split("T")[0],
                    'tech_stack':techName['plain_text'],
                    'entreprise':entreprise_array['plain_text'],
                    'tasks':item['Tasks'][0]['plain_text'] if len(item['Tasks'])>0 else ''
                }
                save_task_from_json(task_data)
                
                entreprise=None
                name=None
                project_name=None
                tech=None
                
                saved_count += 1
            
        return {"success": 200, "saved_items": saved_count}
    except Exception as e:
        return {"error": str(e), "status": 500}