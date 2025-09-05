Site de Receitas - Projeto Django

Este projeto é um site de receitas desenvolvido durante um curso de Django. O objetivo do projeto é permitir que os usuários publiquem, visualizem e pesquisem receitas culinárias de forma prática e organizada.

Funcionalidades

- Listagem de receitas publicadas
- Detalhes de cada receita (ingredientes, modo de preparo, tempo de preparo, etc.)
- Criação, edição e exclusão de receitas (CRUD)
- Categorias para organizar as receitas
- Busca de receitas por termos específicos
- Sistema de autenticação de usuários (login e cadastro)
- Upload de imagens para as receitas

Tecnologias Utilizadas

- Linguagem: Python 3.x
- Framework: Django 4.x
- Banco de dados: SQLite (padrão do Django)
- Front-end: HTML, CSS, Django Templates
- Outras ferramentas: Bootstrap (opcional para estilização), Pillow (para manipulação de imagens)

Pré-requisitos

- Python 3.x instalado
- pip instalado
- Virtualenv recomendado

Instalação

1. Clone o repositório:

git clone https://github.com/wellitondasilvadelima/Projeto_Django.git
cd site-receitas

2. Crie e ative um ambiente virtual:

python -m venv venv
# No Windows
venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate

3. Instale as dependências:

pip install -r requirements.txt

4. Aplique as migrações do banco de dados:

python manage.py migrate

5. Crie um superusuário para acessar o painel administrativo (opcional):

python manage.py createsuperuser

6. Execute o servidor de desenvolvimento:

python manage.py runserver

7. Acesse o site no navegador:

http://127.0.0.1:8000/

Estrutura do Projeto
```
site-receitas/
│
├── authors/          # App para usuários
│   ├── templates/    # Templates HTML
│   ├── static/       # Arquivos estáticos (CSS, JS, imagens)
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   
├── recipes/          # App principal do projeto
│   ├── templates/    # Templates HTML
│   ├── static/       # Arquivos estáticos (CSS, JS, imagens)
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   
│
├── projectDjango/    # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt
```

Licença

Este projeto é apenas para fins de aprendizado durante o curso e não possui licença específica.
