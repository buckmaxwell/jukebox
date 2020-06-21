CREATE TABLE _user.users (
  id serial PRIMARY KEY,
  email varchar,
  service_key varchar, -- the external id assigned by the service
  service varchar,
  profile jsonb,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

