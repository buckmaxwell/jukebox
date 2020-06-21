CREATE TABLE user.users (
  id serial PRIMARY KEY,
  email varchar,
  service_id varchar,
  service varchar,
  profile jsonb,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

