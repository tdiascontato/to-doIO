## Projeto Django - Assistence To-Do via WhatsApp e GPT

### Visão Geral

Este projeto é uma aplicação base em Django que serviria para um acompanhamento completo e se encontra como um assistente pessoal motivacional através de To-Do lists, integrando o WhatsApp e o GPT-3.5 da OpenAI. O objetivo é fornecer orientação e conselhos práticos para o crescimento pessoal dos usuários. A aplicação permite que os usuários se registrem e façam login via WhatsApp, e depois interajam com o sistema para receber conselhos personalizados. A aplicação não está com Clean Code mas pode ser ajustado facilmente, apenas tirando os projetos do papel e fazendo a base. 

### Funcionalidades

1. **Registro de Usuários**
   - Permite que novos usuários se registrem via WhatsApp.
   - Coleta informações essenciais como nome, CPF, senha e número de telefone.

2. **Login de Usuários**
   - Permite que usuários registrados façam login via WhatsApp utilizando CPF e senha.

3. **Integração com GPT-3.5**
   - Recebe contexto e perguntas dos usuários via WhatsApp.
   - Utiliza o modelo GPT-3.5 para gerar respostas motivacionais através de to-do lists práticas.
   - Utiliza de conversas anteriores para personalizar a interação.

4. **Armazenamento de Conversas**
   - Salva todas as interações entre os usuários e o sistema no banco de dados para referência futura.

### Requisitos

- Python 3.x
- Django 3.x ou superior
- Twilio
- OpenAI
- MongoDB
- Decouple (para gerenciar variáveis de ambiente)

### Configuração do Ambiente

1. Clone o repositório:

    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_PROJETO>
    ```

2. Crie um ambiente virtual e instale as dependências:

- Utilização do pipFile para ajudar :)

3. Configure as variáveis de ambiente. Crie um arquivo `.env` na raiz do projeto e adicione as seguintes linhas:

    ```bash
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_WHATSAPP_NUMBER=your_twilio_whatsapp_number
    OPENAI_API_KEY=your_openai_api_key
    ```

4. Realize as migrações do banco de dados:

    ```bash
    python manage.py migrate
    ```

5. Inicie o servidor Django:

    ```bash
    python manage.py runserver
    ```

### Estrutura do Projeto

```plaintext
├── bot
|   ├── migrations
|      ├── __init.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   └── urls.py
├── manage.py
├── db_connection.py
├── Personal_Development
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── Pipfile
```

### Detalhes das Funcionalidades

#### Registro de Usuários

- **Descrição**: Permite que novos usuários se registrem via WhatsApp.
- **Fluxo**:
  1. O usuário envia uma mensagem "NÃO POSSUO CADASTRO".
  2. O sistema solicita informações como nome, CPF, senha e número de telefone.
  3. Após receber todas as informações necessárias, o sistema cria um novo registro de usuário no banco de dados.

#### Login de Usuários

- **Descrição**: Permite que usuários registrados façam login via WhatsApp utilizando CPF e senha.
- **Fluxo**:
  1. O usuário envia uma mensagem com o CPF e a senha.
  2. O sistema verifica as credenciais e, se forem válidas, permite o acesso e registra o horário de login.

#### Integração com GPT-3.5

- **Descrição**: Utiliza o modelo GPT-3.5 da OpenAI para gerar respostas motivacionais e conselhos práticos personalizados.
- **Exemplo de Uso**:
  1. O usuário envia uma mensagem descrevendo sua situação atual ou pedindo conselhos.
  2. O sistema envia o contexto para o GPT-3.5 e recebe uma resposta personalizada, pegando, caso tenha, conversas passadas para ter um maior contexto
  3. A resposta é enviada de volta ao usuário via WhatsApp.

#### Armazenamento de Conversas

- **Descrição**: Salva todas as interações entre os usuários e o sistema no banco de dados para referência futura.
- **Implementação**:
  - Utiliza o modelo `Chats` para armazenar mensagens trocadas, juntamente com o número de telefone do usuário, o corpo da mensagem, o ID da mensagem e o timestamp.
- DB - MongoDB 
