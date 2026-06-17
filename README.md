# Desafio Estágio b2bflow  - Envio de mensagens via Z-API

Script em Python que lê contatos cadastrados no Supabase e envia, via Z-API, a
mensagem `Olá, <nome_contato> tudo bem com você?` para até 3 números. Cada envio
(sucesso ou falha) é registrado na tabela `message_logs`.

## Requisitos

- Python 3.10+
- Conta no [Supabase](https://supabase.com) (plano gratuito)
- Conta na [Z-API](https://z-api.io) com uma instância e WhatsApp conectado

## Setup da tabela

No **SQL Editor** do Supabase, execute o conteúdo de `db/schema.sql` para criar
as tabelas `contacts` e `message_logs` e o enum `message_status`.

Em seguida, ajuste o conteúdo de `db/seed.sql` com seus contatos (telefone no 
formato código do país + DDD + número, apenas dígitos, ex.: `5511999999999`) 
e execute este conteúdo novamente no **SQL Editor** para popular a tabela.


### Tabela `contacts`

Pessoas cadastradas que recebem a mensagem.

| Campo        | Tipo          | Descrição                                          |
| ------------ | ------------- | -------------------------------------------------- |
| `id`         | `uuid`        | Identificador único (gerado automaticamente).      |
| `name`       | `text`        | Nome do contato, usado para personalizar a mensagem. |
| `phone`      | `text`        | Telefone no formato país + DDD + número (só dígitos). |
| `created_at` | `timestamptz` | Data de cadastro do contato.                       |

### Tabela `message_logs`

Histórico de cada tentativa de envio.

| Campo             | Tipo             | Descrição                                              |
| ----------------- | ---------------- | ----------------------------------------------------- |
| `id`              | `uuid`           | Identificador único do registro de envio.             |
| `contact_id`      | `uuid`           | Referência ao contato (`contacts.id`).                |
| `message`         | `text`           | Texto exato da mensagem enviada.                      |
| `zapi_message_id` | `text`           | ID da mensagem retornado pela Z-API.                  |
| `status`          | `message_status` | Resultado do envio: `sent` ou `failed`.               |
| `sent_at`         | `timestamptz`    | Data/hora da tentativa de envio.                      |


## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha:

| Variável            | Onde encontrar                                          |
| ------------------- | ------------------------------------------------------- |
| `SUPABASE_PROJECT_ID` | Supabase → Settings → General → Project ID             |
| `SUPABASE_KEY`        | Supabase → Settings → API Keys → Legacy API keys → `service_role` |
| `ZAPI_INSTANCE_ID`  | Z-API → sua instância → ID                              |
| `ZAPI_TOKEN`        | Z-API → sua instância → Token                           |
| `ZAPI_CLIENT_TOKEN` | Z-API → Segurança da conta → Account Security Token     |


## Como rodar

1. No **SQL Editor** do Supabase, execute `db/schema.sql` e depois `db/seed.sql`
   (ver seção [Setup da tabela](#setup-da-tabela)). Sem isso as tabelas não
   existem e a aplicação falha ao buscar os contatos.
2. Copie `.env.example` para `.env` e preencha as variáveis (ver seção
   [Variáveis de ambiente](#variáveis-de-ambiente)).
3. Crie o ambiente virtual, instale as dependências e rode:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

No Linux/macOS, ative o venv com `source .venv/bin/activate`.

## Logs

A aplicação registra logs em duas camadas:

- **Operacional**: console (stdout) e arquivo local `app.log`: Registra execução do fluxo, envios e erros.
- **Negócio**: tabela `message_logs` no Supabase: Registra cada mensagem enviada com seu
  status (`sent` ou `failed`).
