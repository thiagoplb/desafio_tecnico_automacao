create type message_status as enum ('sent', 'failed');

create table if not exists contacts (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  phone text not null,
  created_at timestamptz not null default now()
);

create table if not exists message_logs (
  id uuid primary key default gen_random_uuid(),
  contact_id uuid not null references contacts(id),
  message text not null,
  zapi_message_id text,
  status message_status not null default 'sent',
  sent_at timestamptz not null default now()
);
