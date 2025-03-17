# Desafio banco de talentos

Sua tarefa é construir uma aplicação que expõe uma API RESTful para gerenciar perfis de talentos. A aplicação deve permitir que os usuários se cadastrem, atualizem seus perfis e que qualquer pessoa interessada possa listar e, se necessário, filtrar os perfis cadastrados.

A aplicação deve ser construída utilizando **Python**. Você pode utilizar qualquer banco de dados, frameworks, bibliotecas e ferramentas de sua preferência. Esperamos que você explique as decisões tomadas durante o desenvolvimento e os motivos de suas escolhas.

## Critérios de Aceitação
- README.md contendo informações básicas do projeto e instruções de execução
- A API deve ser RESTful, real e escrita por você. Ferramentas que criam APIs automaticamente não serão aceitas (Por exemplo, json-server)
- Todos os requisitos abaixo devem ser cumpridos, seguindo o padrão de rotas estabelecido
- Deve haver uma documentação descrevendo sua API
- Se você julgar necessário, adequado ou quiser deixar a aplicação mais completa (bônus!) você pode adicionar outras rotas, métodos etc
- As modelagens de resposta são sugestões e você pode alterá-las conforme achar melhor
- A aplicação deve ser escrita em Python
- A aplicação deve fazer requisições a um banco de dados para persistência

# Requisitos

## 0: A API deve responder em uma porta de sua escolha.

## 1: Cadastro de Perfil de Talento

`POST /profiles Content-Type: application/json`
```json
{
  "name": "Nome do Talento",
  "email": "talento@example.com",
  "phone": "123456789",
  "location": "Cidade, Estado",
  "linkedin_prorfile": "https://linkedin.com/in/profile",
  "github_profile": "https://github.com/profile",
  "skills": ["Python", "Machine Learning", "Data Science"],
  "experience": "Breve descrição das experiências profissionais",
  "education": "Informações sobre a formação acadêmica",
  "idioms": ["Portuguese", "English", "Spanish"],
  "bio": "Uma breve descrição sobre o talento",
  "open_to_work": true
}
```

Reposta:
```json
{
  "id": 1,
  "name": "Nome do Talento",
  "email": "talento@example.com",
  "phone": "123456789",
  "location": "Cidade, Estado",
  "linkedin_prorfile": "https://linkedin.com/in/profile",
  "github_profile": "https://github.com/profile",
  "skills": ["Python", "Machine Learning", "Data Science"],
  "experience": "Breve descrição das experiências profissionais",
  "education": "Informações sobre a formação acadêmica",
  "idioms": ["Portuguese", "English", "Spanish"],
  "bio": "Uma breve descrição sobre o talento",
  "open_to_work": true,
  "created_at": "<data de criação>"
}
```

## 2: Listagem dos Perfis de Talentos
`GET /profiles` <br>
`GET /profiles?open_to_work=true`

Resposta:
```json
[
  {
    "id": 1,
    "name": "Nome do Talento",
    "email": "talento@example.com",
    "phone": "123456789",
    "location": "Cidade, Estado",
    "linkedin_prorfile": "https://linkedin.com/in/profile",
    "github_profile": "https://github.com/profile",
    "skills": ["Python", "Machine Learning", "Data Science"],
    "experience": "Breve descrição das experiências profissionais",
    "education": "Informações sobre a formação acadêmica",
    "idioms": ["Portuguese", "English", "Spanish"],
    "bio": "Uma breve descrição sobre o talento",
    "open_to_work": true,
    "created_at": "<data de criação>"
  },
  {
    "id": 2,
    "name": "Outro Talento",
    "email": "outrotalento@example.com",
    "phone": "987654321",
    "location": "Outra Cidade, Estado",
    "linkedin_prorfile": "https://linkedin.com/in/profile",
    "github_profile": "https://github.com/profile",
    "skills": ["JavaScript", "React", "Node.js"],
    "experience": "Resumo das experiências anteriores",
    "education": "Detalhes da formação acadêmica",
    "idioms": ["Portuguese", "English", "Spanish"],
    "bio": "Descrição breve sobre o perfil",
    "open_to_work": true,
    "created_at": "<data de criação>"
  }
  ...
]
```
Exemplo de filtros mais complexos (possíveis bônus): <br>
`GET /profiles?filter[skills]=Python` <br>
`GET /profiles?filter[idioms]=Engilsh,Portuguese` <br>
`GET /profiles?filter[skills]=Python&open_to_work=true`

## 3: Atualização de Perfil de Talento
`PUT /profiles/:profile_id Content-Type: application/json`
```json
{
  "bio": "Nova descrição atualizada sobre o talento",
  "skills": ["Python", "Deep Learning", "Data Science"]
}
```

Resposta:
```json
{
  "id": 1,
  "name": "Nome do Talento",
  "email": "talento@example.com",
  "phone": "123456789",
  "location": "Cidade, Estado",
  "linkedin_prorfile": "https://linkedin.com/in/profile",
  "github_profile": "https://github.com/profile",
  "skills": ["Python", "Machine Learning", "Data Science"],
  "experience": "Breve descrição das experiências profissionais",
  "education": "Informações sobre a formação acadêmica",
  "idioms": ["Portuguese", "English", "Spanish"],
  "bio": "Uma breve descrição sobre o talento",
  "open_to_work": true,
  "created_at": "<data de criação>"
}
```

# Bonus
Os seguintes itens não são obrigatórios, mas poderão agregar valor à sua submissão (os itens em negrito são considerados mais significativos):

- **Filtros mais complexos na listagem de perfil de candidatos**
- **Testes Automatizados**
- **Containerização da Aplicação**
- **Separação entre configuração do App e código**
- Funcionalidade de upload e download de CV através da API (file storage)
- Segurança da API
- Otimização e Boas Práticas
- Pipelines de CI
- Uso de Cloud Providers
