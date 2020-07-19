CREATE TABLE authorizer.authorizations (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4 (),
  access_token varchar,
  refresh_token varchar,
  scope varchar,
  service varchar,
  access_token_expiration timestamp,
  created_at timestamp DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp
);

