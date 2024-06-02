from django.db import models
from db_connection import db

Users = db['Users']
# _id | name | cpf | secret
Chats = db['Chats']
# _id | user | phone_user | body | message_id

