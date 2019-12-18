import os, getpass

class SysUtils:

  @staticmethod
  def get_current_username():
    return getpass.getuser()

  @staticmethod
  def get_env_var_val(env_var):
    return os.environ.get(env_var)