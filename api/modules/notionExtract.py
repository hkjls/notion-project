from datetime import datetime
import pytest
# import sys
# from pathlib import Path

# root = Path(__file__).resolve().parent.parent.parent
# sys.path.append(str(root))
from base.models import Task

def save_task_from_json(json_data):
    """
    Save task data from JSON format to the database
    json_data should contain: tasks, date, projects
    Optional fields: clients, entreprise, tech_stack, done
    """
    try:
        # Convert date string to date object if it's a string
        date = json_data.get('date')
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()

        # Create task instance
        task = Task(
            tasks=json_data['tasks'],
            date=date,
            projects=json_data['projects'],
            done=json_data.get('done', False),
            clients=json_data.get('clients'),
            entreprise=json_data.get('entreprise'),
            tech_stack=json_data.get('tech_stack')
        )
        
        # Save to database
        task.save()
        return task
    
    except KeyError as e:
        raise ValueError(f"Missing required field: {e}")
    except Exception as e:
        raise Exception(f"Error saving task: {e}")
