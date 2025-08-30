from notion_client import Client
from .saveNotionData import save_task_from_json

class notion:
    def __init__(self, api_key:str=""):
        if api_key=="":
            print("Your API Key is empty")
            self.getAccess = ""
            exit()
        self.getAccess = Client(auth=api_key)
    
    def get_dbs(self):
        response = self.getAccess.search(
            filter={
                "property":"object",
                "value":"database"
            }
        )
        
        return response
    
    def get_db(self, db_name:str=""):
        #Filter the response by the database name
        db_id = next(
            (item['id'] for item in self.get_dbs()['results'] 
             if item['title'][0]['text']['content'] == db_name),
            None
        )
        #Send the request to have the content database
        next_cursor = None
        has_more = True
        
        while has_more:
            db_content = self.getAccess.databases.query(
                database_id=db_id,
                start_cursor=next_cursor,
                page_size=20,
                sorts=[{"property":"Date","direction":"descending"}]
            )
            
            has_more=db_content["has_more"]
            next_cursor=db_content['next_cursor']
            
            data = {
                "data": [{
                    "id": page['id'],
                    "properties": {
                        key:value[value['type']]
                        for key, value in page['properties'].items()
                    }
                } for page in db_content['results']]
            }
            
            entreprise=None
            name=None
            project_name=None
            tech=None
            
            for item in data['data']:
                id=item['id']
                item = item['properties']

                entreprise_array = {'plain_text':""}
                name_title={'plain_text':""}
                projectName = {'plain_text':""}
                techName = {'plain_text':""}
                
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
        
        return {"success": 200}