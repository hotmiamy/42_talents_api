# Desafio banco de vagas
Sua tarefa é construir uma aplicação que expõe uma API RESTful que serve para gerenciar vagas de emprego. A aplicação deve permitir que os administradores possam cadastrar, listar, atualizar e deletar vagas de emprego. Além disso, deve ser possível listar as vagas de emprego disponíveis e filtrar por diferentes critérios.

A aplicação deve ser construída utilizando **Python**. Pode ser utilizado qualquer banco de dados, frameworks, bibliotecas e ferramentas de sua preferência. Esperamos que você explique as decisões que tomou durante o desenvolvimento e o motivo de suas escolhas.

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

## 0: A API deve responder em uma porta exposta a sua escolha.

## 1: Deve ser possível cadastrar uma empresa
`POST /companies Content-Type: application/json`
```json
{
	"name": "Company Name",
	"industry": "Technology",
	"size": "Medium",
	"location": "São Paulo",
	"website": "https://company.com",
	"description": "A brief description about the company"	
}
```

Resposta:
```json
{
	"id": 1,
	"name": "Company Name",
	"industry": "Technology",
	"size": "Medium",
	"location": "São Paulo",
	"website": "https://company.com",
	"description": "A brief description about the company",
	"created_at": "<date of creation>"
}
```

## 2: Deve ser possível listar as empresas cadastradas
`GET /companies`

Resposta:
```json
[
	{
		"id": 1,
		"name": "Company Name",
		"industry": "Technology",
		"size": "Medium",
		"location": "São Paulo",
		"website": "https://company.com",
		"description": "A brief description about the company",
		"created_at": "<date of creation>"
	},
	{
		"id": 2,
		"name": "Other Company Name",
		"industry": "Finance",
		"size": "Large",
		"location": "Rio de Janeiro",
		"website": "https://othercompany.com",
		"description": "A brief description about the other company",
		"created_at": "<date of creation>"
	},
	...
]
```

## 3: Deve ser possível cadastrar uma vaga de emprego
`POST /companies/:company_id/jobs Content-Type: application/json`
```json
{
	"title": "Job Title",
	"level": "Junior",
	"type": "CLT",
	"requirements": ["Python", "Django", "RESTful APIs"],
	"deadline": "2021-12-31",
	"status": "open",
	"description": "A brief description about the job"
}
```

Resposta:
```json
{
	"id": 1,
	"title": "Job Title",
	"company_id": 1,
	"location": "São Paulo",
	"level": "Junior",
	"type": "CLT",
	"requirements": ["Python", "Django", "RESTful APIs"],
	"deadline": "2021-12-31",
	"status": "open",
	"created_at": "<date of creation>"
}
```

## 4: Deve ser possível listar as vagas de emprego cadastradas
`GET /jobs`

Resposta:
```json
[
	{
		"id": 1,
		"title": "Job Title",
		"company_id": 1,
		"location": "São Paulo",
		"level": "Junior",
		"type": "CLT",
		"requirements": ["Python", "Django", "RESTful APIs"],
		"deadline": "2021-12-31",
		"status": "open",
		"created_at": "<date of creation>"
	},
	{
		"id": 2,
		"title": "Other Job Title",
		"company_id": 2,
		"location": "Rio de Janeiro",
		"level": "Senior",
		"type": "PJ",
		"requirements": ["Java", "Spring Boot", "Microservices"],
		"deadline": "2021-12-31",
		"status": "open",
		"created_at": "<date of creation>"
	},
	...
]
```

## 5: Deve ser possível alterar o status de uma vaga de emprego
`PUT /jobs/:job_id/status Content-Type: application/json`
```json
{
	"status": "closed"
}
```

## Bônus
Os seguintes itens não são obrigatórios, mas darão mais valor ao seu trabalho (os em negrito são mais significativos para nós)

- **Testes**
- **Containerização da aplicação**
- **Separação entre configuração do App e código**
- **Segurança da API com autenticação e autorização**
- Cuidados especiais com otimização, padrões, entre outros
- Filtros mais complexos na listagem de vagas e/ou empresas
- Pipelines de CI
- Utilização de algum cloud provider (AWS, GCP, Azure...)
