import pdb

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from decouple import config
import json

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = 'whatsapp:+14155238886'

client = Client(account_sid, auth_token)

def home(request):
    return HttpResponse("Hello, world.")

def send_whatsapp_message(to, body):
    message = client.messages.create(
        body=body,
        from_=twilio_whatsapp_number,
        to=f'whatsapp:+{to}'
    )
    return message.sid

def send_message(request):
    to = request.GET.get('to')
    body = request.GET.get('body')
    if to and body:
        try:
            message_sid = send_whatsapp_message(to, body)
            return JsonResponse({"message_sid": message_sid}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Please provide 'to' and 'body' parameters."}, status=400)


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        process_message(data)
        return JsonResponse({"status": "success"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)

def process_message(data):
    message = data['messages'][0]
    phone_number = message['from']
    message_body = message['body']

    # Simple logic to respond to specific messages
    if message_body.lower() == 'oi':
        send_whatsapp_message(phone_number, "Olá! Como posso ajudar?")
    elif message_body.lower() == 'tchau':
        send_whatsapp_message(phone_number, "Tchau! Até a próxima.")
    else:
        send_whatsapp_message(phone_number, "Desculpe, não entendi sua mensagem.")
