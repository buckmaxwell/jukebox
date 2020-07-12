CREATE TABLE _user.users (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  email varchar,
  service_key varchar, -- the external id assigned by the service, ie spotify id
  service varchar,
  profile jsonb,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

