-- Create extensions
create extension if not exists "uuid-ossp";

-- Create enum types
create type campaign_status as enum ('draft', 'active', 'paused', 'completed', 'cancelled');
create type call_status as enum ('pending', 'in_progress', 'completed', 'failed', 'no_answer');

-- Create campaigns table
create table if not exists campaigns (
    id uuid primary key default uuid_generate_v4(),
    name varchar(255) not null,
    description text,
    status campaign_status default 'draft',
    schedule_start timestamp with time zone,
    schedule_end timestamp with time zone,
    script_template text,
    max_retries integer default 3,
    retry_delay_minutes integer default 60,
    total_calls integer default 0,
    successful_calls integer default 0,
    failed_calls integer default 0,
    pending_calls integer default 0,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create contact_lists table
create table if not exists contact_lists (
    id uuid primary key default uuid_generate_v4(),
    name varchar(255) not null,
    description text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create contacts table
create table if not exists contacts (
    id uuid primary key default uuid_generate_v4(),
    phone_number varchar(20) not null,
    name varchar(255),
    email varchar(255),
    additional_data jsonb default '{}',
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create contact_list_contacts junction table
create table if not exists contact_list_contacts (
    contact_list_id uuid references contact_lists(id) on delete cascade,
    contact_id uuid references contacts(id) on delete cascade,
    created_at timestamp with time zone default now(),
    primary key (contact_list_id, contact_id)
);

-- Create campaign_contact_lists junction table
create table if not exists campaign_contact_lists (
    campaign_id uuid references campaigns(id) on delete cascade,
    contact_list_id uuid references contact_lists(id) on delete cascade,
    created_at timestamp with time zone default now(),
    primary key (campaign_id, contact_list_id)
);

-- Create calls table
create table if not exists calls (
    id uuid primary key default uuid_generate_v4(),
    campaign_id uuid references campaigns(id) on delete cascade,
    contact_id uuid references contacts(id) on delete cascade,
    status call_status default 'pending',
    duration_seconds integer,
    attempt_count integer default 0,
    last_attempt_at timestamp with time zone,
    next_attempt_at timestamp with time zone,
    notes text,
    recording_url text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create indexes
create index idx_campaigns_status on campaigns(status);
create index idx_calls_status on calls(status);
create index idx_calls_campaign_id on calls(campaign_id);
create index idx_calls_contact_id on calls(contact_id);
create index idx_contacts_phone_number on contacts(phone_number);

-- Create updated_at trigger function
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

-- Create triggers for updated_at
create trigger update_campaigns_updated_at
    before update on campaigns
    for each row
    execute function update_updated_at_column();

create trigger update_contact_lists_updated_at
    before update on contact_lists
    for each row
    execute function update_updated_at_column();

create trigger update_contacts_updated_at
    before update on contacts
    for each row
    execute function update_updated_at_column();

create trigger update_calls_updated_at
    before update on calls
    for each row
    execute function update_updated_at_column();
