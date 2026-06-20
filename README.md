# Desafio b2bflow — Supabase + Z-API

Script Python que lê contatos do Supabase e envia mensagem personalizada via Z-API.

## Setup da tabela (Supabase)

```sql
create table contatos (
  id uuid primary key default gen_random_uuid(),
  nome text not null,
  contato text not null,
  created_at timestamp default now()
);

alter table contatos enable row level security;

create policy "ler_contatos"
on contatos
for select
using (true);
```

> `contato` no formato DDI+DDD+número, <br> Ex: `5587991234567`.

## Variáveis de ambiente (.env)

```
SUPABASE_URL=
SUPABASE_KEY=
ZAPI_INSTANCE=
ZAPI_TOKEN=
ZAPI_KEY=
```

## Como rodar 
- Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

## Como rodar 
- Windows

```bash
python -m venv venv
venv\Scripts\activate         
pip install -r requirements.txt
python main.py
```