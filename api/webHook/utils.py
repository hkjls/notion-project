import requests
import json
import logging

logger = logging.getLogger(__name__)

def send_webhook_notification(target_url: str, payload: dict, secret_token:str = None):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    if secret_token:
       headers['X-Webhook-Secret'] = secret_token
    try:
        response = requests.post(target_url, headers=headers, data=json.dumps(payload), timeout=5)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        logger.info(f"Webhook successfully sent to {target_url}. Status: {response.status_code}")
        logger.debug(f"Response: {response.text}")
        return True
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Webhook failed: Could not connect to {target_url}. Error: {e}")
        return False
    except requests.exceptions.Timeout:
        logger.error(f"Webhook failed: Request to {target_url} timed out.")
        return False
    except requests.exceptions.HTTPError as e:
        logger.error(f"Webhook failed: HTTP error for {target_url}. Status: {e.response.status_code}, Response: {e.response.text}")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred while sending webhook to {target_url}. Error: {e}")
        return False