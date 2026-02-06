create table public.user_gamification (
  user_id uuid primary key references auth.users(id) on delete cascade,
  koin integer not null default 0,
  xp integer not null default 0,
  level integer not null default 1,
  streak_days integer not null default 0,
  last_checkin_date timestamp with time zone,
  daily_target integer not null default 1,
  created_at timestamp with time zone not null default now(),
  updated_at timestamp with time zone not null default now()
);

-- RLS Policies
alter table public.user_gamification enable row level security;

create policy "Users can view own gamification data"
  on public.user_gamification for select
  using (auth.uid() = user_id);

create policy "Users can insert own gamification data"
  on public.user_gamification for insert
  with check (auth.uid() = user_id);

create policy "Users can update own gamification data"
  on public.user_gamification for update
  using (auth.uid() = user_id);

-- Index
create index idx_user_gamification_user_id on public.user_gamification(user_id);

-- Trigger for updated_at (assuming update_updated_at_column function exists, if not we create it)
create or replace function update_updated_at_column()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger update_user_gamification_updated_at
  before update on public.user_gamification
  for each row
  execute function update_updated_at_column();
