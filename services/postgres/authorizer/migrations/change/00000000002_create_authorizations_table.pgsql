create table authorizer.authorizations(
  id serial primary key,
  
  access_token varchar,
  refresh_token varchar,
  scope varchar,
  service varchar,
  access_token_expiration timestamp,

  created_at timestamp default current_timestamp,
  updated_at timestamp default current_timestamp,
  deleted_at timestamp
);