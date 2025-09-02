import requests

def send_request():
    endpoint = "http://localhost:8000/api/auth/token/"
    response = requests.post(
        endpoint,
        json={
            'username':'Joelas',
            'password':'admin'
        }
    )
    
    Token = response.json()['token']
    
    endpoint_tasks = "http://localhost:8000/api/base/tasks/"
    headers = {
        "Authorization": f"Token {Token}"
    }
    tasks_list = requests.get(
        endpoint_tasks,
        headers=headers
    )
    
    print(tasks_list.json())
    return

if __name__ == "__main__":
    send_request()