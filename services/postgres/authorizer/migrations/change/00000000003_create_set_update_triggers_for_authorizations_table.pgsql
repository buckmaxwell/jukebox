CREATE TRIGGER set_authorizations_updated_at
  BEFORE UPDATE ON authorizer.authorizations
  FOR EACH ROW
  EXECUTE PROCEDURE trigger_set_updated_at();
