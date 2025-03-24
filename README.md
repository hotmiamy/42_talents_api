# Projeto Talent

Este projeto é uma API desenvolvida com Flask para gerenciamento de perfis, oferecendo funcionalidades como criação, atualização, upload/download de currículos e filtros avançados. A API utiliza SQLAlchemy como ORM, autenticação JWT para rotas protegidas e validações com Marshmallow.

## Sumário

- [Recursos](#recursos)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Rodando a Aplicação](#rodando-a-aplicação)
- [Testes](#testes)

## Recursos

- **CRUD de Perfis:** Criação, listagem, atualização e obtenção de perfis.
- **Upload e Download de Currículos:** Upload de arquivos PDF com validações (tipo e tamanho) e download dos currículos.
- **Autenticação JWT:** Rotas protegidas para operações críticas.
- **Filtros Avançados:** Filtragem por skills, idiomas e localização.
- **Validações com Marshmallow:** Validações de dados na criação e atualização de perfis.

## Tecnologias Utilizadas

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
- [psycopg2](https://www.psycopg.org/) (para conexão com PostgreSQL)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- Docker e Docker Compose

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/projeto-talent.git
   cd projeto-talent
    ```
2. **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. **Instale as dependências:**
    ```bash
    pip install -r config/requirements.txt
    ```

## Configurações

O projeto utiliza variáveis de ambiente definidas no arquivo .env. Um exemplo de arquivo .env:

```.env
FLASK_APP=app/app.py
FLASK_DEBUG=1
DATABASE_URL=postgresql://user:password@localhost:5432/talent_db
FLASK_ENV=development
JWT_SECRET_KEY=1234
FLASK_SECRET_KEY=secret-key
DB_USER=user
DB_PASSWORD=1234
DB_NAME=talent_db
UPLOAD_FOLDER=uploads
```

## Rodando a Aplicação

**localmente**

1. **Inicialize o banco de dados (caso utilize PostgreSQL, certifique-se de que o servidor esteja ativo):**

    ```bash
    flask run
    ```
2. A aplicação estará disponível na porta 5000.

**Com Docker**

1. **Construa e execute os containers:**
    ```bash
    docker compose up --build
    ```
2. A aplicação estará disponível na porta 5000.

## Testes

O projeto utiliza o pytest para execução dos testes. Para rodar os testes, utilize:

```bash
pytest
```
Durante os testes, a configuração do banco de dados é sobrescrita para utilizar o SQLite em memória. Se necessário, ajuste a função create_app para não tentar conectar ao PostgreSQL quando a flag TESTING estiver ativa.

