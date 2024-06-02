import json
import pdb

from datetime import datetime, timedelta

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from twilio.rest import Client
from .models import Users, Chats
from decouple import config

#config Twilio
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = config('TWILIO_WHATSAPP_NUMBER')
client = Client(account_sid, auth_token)


# /bot/home
def home(request):
    users_html = "<h3>Hello!</h3>"
    return HttpResponse(users_html)


########## twilio_webhook && GPT ##########
@csrf_exempt
def twilio_webhook(request):
    if request.method == 'POST':
        from_number = request.POST.get('WaId')
        body = request.POST.get('Body').strip()
        user = Users.find_one({'number_phone': from_number})

        body_lines = body.split('\n')
        data = {}

        # Caso login recente
        if login_time(user):
            gpt_response = get_gpt_response(body)
            send_message(from_number, gpt_response)
            Chats.insert_one({
                "user": user['name'],
                "phone_user": from_number,
                "body": body+'|'+gpt_response,
                "message_id": request.POST.get('SmsMessageSid'),
                "timestamp": datetime.now(),
            })
            return HttpResponse(f"Mensagem salva", status=200)
        # Caso não tenha cadastro
        if 'NÃO POSSUO CADASTRO' in body:
            try:  # Adicionar user
                for line in body_lines[1:]:
                    key, value = line.split(':')
                    data[key.strip().lower()] = value.strip()
                # Verificar se todos os campos necessários estão presentes
                required_fields = ['name', 'cpf', 'password', 'number_phone']
                if all(field in data for field in required_fields):
                    data['name'] = data['name'].split()[0]
                    add_user(data)
                    send_message(from_number, "Conta criada com sucesso. Tente fazer o login!")
                    first_message(from_number)
                else:
                    send_message(from_number, "Não foi possível compreender. Por favor, siga as instruções.")
                    first_message(from_number)
            except Exception as e:
                send_message(from_number, f"Erro ao processar cadastro: {str(e)}")
        # Caso tenha cadastro
        else:
            try:  # Fazer Login
                for line in body_lines:
                    key, value = line.split(':')
                    data[key.strip().lower()] = value.strip()
                if 'cpf' in data and 'password' in data:
                    if login(data['cpf'], data['password']):
                        gpt_response = get_gpt_response(body)
                        send_message(from_number, gpt_response)
                        Chats.insert_one({
                            "user": user['name'],
                            "phone_user": from_number,
                            "body": body+'|'+gpt_response,
                            "message_id": request.POST.get('SmsMessageSid'),
                            "timestamp": datetime.now(),
                        })
                        return HttpResponse(f"Mensagem salva", status=200)
                    else:
                        send_message(from_number, "CPF ou senha incorretos. Por favor, tente novamente.")
                        first_message(from_number)
                else:
                    send_message(from_number, "Não foi possível compreender. Por favor, siga as instruções.")
                    first_message(from_number)
            except Exception as e:
                send_message(from_number, "Erro ao processar login, por favor tente novamente:")
                first_message(from_number)
                print(e)

    return HttpResponse("Quebra Twilio Webhook", status=405)


# GPT request
def get_gpt_response(context):
    client = OpenAI(api_key=config('OPENAI_API_KEY'))
    prompt = f'''
    Você é um assistente pessoal altamente qualificado para fornecer orientação e conselhos práticos para o crescimento pessoal. A pessoa que você está ajudando está passando por {context}.
    Com base no que foi compartilhado, você deve oferecer conselhos úteis e incentivadores para ajudá-la a enfrentar desafios, superar obstáculos e alcançar seus objetivos. Lembre-se de ser empático, motivador e direto em suas sugestões.
    Seu conselho deve ser prático, acionável e personalizado para a situação específica. Concentre-se em fornecer soluções realistas e estratégias que possam ser implementadas imediatamente para promover o crescimento pessoal e o desenvolvimento contínuo.
    O resumo do conselho deve ser claro, conciso e inspirador, com um máximo de 300 caracteres. Utilize uma linguagem acessível e positiva para transmitir suas mensagens de apoio e encorajamento.
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


########## Assets Functions##########
# Get all Users
def get_all_users():
    users = list(Users.find({}))
    return users


# /bot/send_message
@csrf_exempt
def send_message(to, body):
    try:
        message = client.messages.create(
            from_=twilio_whatsapp_number,
            to=f'whatsapp:+{to}',
            body=body,
        )
        return JsonResponse({"message_sid": message.sid}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def login_time(user):
    if 'login' in user and user['login'] < datetime.now() - timedelta(hours=2):
        return False
    return bool(user)


def date_update(user):
    user['login'] = datetime.now()
    Users.update_one({'_id': user['_id']}, {"$set": user})
    return bool(user)


def first_message(phone_user):
    message = (
        "Olá, faça seu login como o exemplo!\nCPF:12312312322\nPASSWORD:121212\n\nSenão possuir cadastro, envie: NÂO POSSUO CADASTRO\nNAME:\nCPF:\nPASSWORD:\nNUMBER_PHONE:")
    send_message(phone_user, message)


########## Mains Functions ##########
# Add user
@csrf_exempt
def add_user(request=None, data=None):
    if request is not None:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({"error": f"Erro ao decodificar JSON: {str(e)}"}, status=400)

    if data is not None:
        try:
            user = {
                "name": data['name'].strip(),
                "cpf": data['cpf'].strip(),
                "password": data['password'].strip(),
                "number_phone": data['number_phone'].strip(),
                "login": datetime.now(),
            }
            Users.insert_one(user)
            return JsonResponse({"success": f"Sucesso ao salvar {data['name']}", "data": data}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method or missing data"}, status=400)


# Login
def login(cpf, password):
    user = Users.find_one({'cpf': cpf, 'password': password})
    if user:
        date_update(user)
    return bool(user)