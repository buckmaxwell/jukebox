create table user.users(
  id serial primary key,

  email varchar,
  service varchar,
  profile jsonb,

  created_at timestamp default current_timestamp,
  updated_at timestamp default current_timestamp,
  deleted_at timestamp
);
