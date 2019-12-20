# Consts
from src.consts.servers.main import HTTPConsts

class AccountsAuthEntity:

  @staticmethod
  def do_auth():
    pass

  @staticmethod
  def is_authed(auth_token):
    if auth_token == HTTPConsts.STATIC_AUTH_TOKEN:
      return True
    return False