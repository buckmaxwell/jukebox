CREATE TRIGGER set_users_updated_at
  BEFORE UPDATE ON _user.users
  FOR EACH ROW
  EXECUTE PROCEDURE trigger_set_updated_at ();

