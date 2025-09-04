from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import send_webhook_notification
# Create your views here.

@csrf_exempt
def receive_webhook(request):
    if request.method == 'POST':
        # Traitez les données reçues
        data = request.body.decode('utf-8')
        print(f"Webhook reçu avec les données:")
        print(json.dumps(data, indent=4))
        
        if 'event_type' in data:
            print(f"Event Type: {data['event_type']}")
        if 'payload' in data and 'message' in data['payload']:
            print(f"Message: {data['payload']['message']}")
                
        return JsonResponse({'status': 'success', 'message': 'Webhook reçu'})
    else:
        return HttpResponseBadRequest('Méthode non autorisée')
    
def trigger_local_webhook(request):
    if request.method == 'GET':
        target_url = request.build_absolute_uri('/api/webhook/webhook-receiver/')
        payload = {
            'event_type': 'test_notification',
            'timestamp': '2025-09-04T10:00:00Z', # Example data
            'payload': {
                'message': 'This is a test message from Django sender!',
                'source': 'local_django_sender',
                'user_id': 123
            }
        }
        
        success = send_webhook_notification(target_url, payload, secret_token="my_secret_123")

        if success:
            return HttpResponse("Webhook sent successfully to local receiver!", status=200)
        else:
            return HttpResponse("Failed to send webhook to local receiver. Check logs.", status=500)
    return HttpResponse("This endpoint only supports GET requests for triggering.", status=405)