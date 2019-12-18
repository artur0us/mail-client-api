class AccountsAuthEntity:

  @staticmethod
  def do_auth():
    pass

  @staticmethod
  def is_authed(auth_token):
    if auth_token == "uuid_token":
      return True
    return False