# API de Ocorrências de Veículo

> Permite gerar ocorrências sempre que um veículo da frota sofre uma avaria, uma multa, ou precisa de manutenção.
> A aplicação permite listar e deletar as ocorrências. Não depende de nenhum repositório privado, credencial
ou integração externa real de negócio (SAP, Bluefleet, Equals, DocuSign). Tudo
roda local.

---

## Persistência
Não foi utilizado banco de dados real. As ocorrências são guardadas em uma
estrutura em memória: `list\[dict]` dentro de `model/repository.py`

---
## Layout

```
desafio-junior/
├──src/
│   ├──client/
│   │    └──cep_client.py                       # chamada HTTP à API pública de CEP (ViaCEP)
│   ├──config/
│   │    └──settings.py                         # configurações (Pydantic BaseSettings)
│   ├──manager/
│   │    └──ocorrencia_manager.py               # regra de negócio / orquestração
│   ├──model/
│   │    ├──schema/
│   │    │   └──ocorrencia.py                   # schemas Pydantic (entrada e saída)
│   │    └──repository.py                       # "banco de dados" em memória
│   ├──route/
│   │    ├──endpoint/
│   │    │   └──ocorrencia.py                   # endpoints HTTP (fino: só valida e orquestra)
│   │    └──api.py                              # registra os blueprints
│   ├──tests/
│   │    ├──resources/
│   │    │   └──ocorrencia_payload.json         # payload utilizado nos testes
│   │    ├──conftest.py                         # fixtures compartilhadas (client, mock de CEP, payload)
│   │    └──test_ocorrencia.py                  # testes unitários da aplicação
│   ├──utils/
│   │    └──json_response.py                    # estrutura das respostas em json
│   └──app.py                                   # cria e sobe a aplicação flask
├──pyproject.toml
└──README.md
```
---

## Stack:
* Python 3.13
* Flask
* Pydantic v2
* Pytest

---


## Instalação

### 1. Pré requisitos:
    Python 3.13 instalado

### 2. Clone o repositório e entre na pasta:
    cd desafio-junior

### 3. Crie e ative o ambiente virtual:
    python3.13 -m venv .venv
    source .venv/bin/activate        # Linux/Mac
    .venv\Scripts\activate           # Windows

### 4. Instale as dependências (incluindo as de desenvolvimento/teste)
    pip install -e ".[dev]" 

---

## Rodar a aplicação

    python src/app.py

---

## Testes

Os testes usam um cliente de testes do Flask (sem precisar do servidor rodando) e mockam a chamada à API do ViaCEP — não
dependem de acesso à internet.

### Para rodar os testes:

    pytest src/tests/test_ocorrencia.py -v

---

## Observações

* A única chamada de rede real prevista é à API pública do ViaCEP, usada para completar o endereço a partir do CEP informado.

* Erros de validação e falhas na consulta de CEP nunca expõem _stacktrace_ ao cliente da API — sempre retornam uma mensagem de erro clara em JSON.

## Funcionalidades

### 1. Schema de validação (`model/schema/ocorrencia.py`)


|Campo|Tipo|Regra|
|-|-|-|
|`placa`|`str`|obrigatório, formato `AAA9A99` ou `AAA9999`|
|`tipo`|`Literal`|obrigatório, AVARIA, MANUTENCAO ou MULTA|
|`descricao`|`str`|obrigatório, `min_length=5`, `max_length=255`|
|`dataOcorrencia`|`date`|obrigatório, não pode ser data futura|
|`cep`|`str`|obrigatório, 8 dígitos,com ou sem máscara|


## Endpoints
`POST /ocorrencia`

Cria nova ocorrência

**Corpo da requisição:**

```json
{
  "placa": "ABC1D23",
  "tipo": "AVARIA",
  "descricao": "Amassado na porta do motorista",
  "dataOcorrencia": "2025-01-15",
  "cep": "01310-100"
}
```

**Resposta de sucesso (`201`):**

```json
{
  "success": true,
  "data": {
    "id": "a1b2c3d4-...",
    "placa": "ABC1D23",
    "tipo": "AVARIA",
    "descricao": "Amassado na porta do motorista",
    "dataOcorrencia": "2025-01-15",
    "endereco": {
      "logradouro": "Avenida Paulista",
      "bairro": "Bela Vista",
      "localidade": "São Paulo",
      "uf": "SP"
    }
  }
}
```
**Resposta de erro (`400`)** — payload inválido ou CEP não encontrado:

```json
{
  "success": false,
  "message": "CEP inválido. Use o formato 99999999 ou 99999-999"
}
```

### `GET /ocorrencia/<placa>`

Lista todas as ocorrências registradas para a placa informada. Retorna lista vazia (não é erro) se não houver ocorrências.

**Resposta (`200`):**

```json
{
  "success": true,
  "data": [
    {
      "id": "a1b2c3d4-...",
      "placa": "ABC1D23",
      "tipo": "AVARIA",
      "descricao": "Amassado na porta do motorista",
      "dataOcorrencia": "2025-01-15",
      "endereco": { "...": "..." }
    }
  ]
}
```

### `DELETE /ocorrencia/<id>`

Remove uma ocorrência pelo seu `id`.

**Resposta de sucesso (`200`):**

```json
{ "success": true, "data": { "id": "a1b2c3d4-..." } }
```

**Resposta de erro (`404`)** — id não encontrado:

```json
{ "success": false, "message": "Ocorrência não encontrada" }
```
