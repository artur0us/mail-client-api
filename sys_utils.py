import os, getpass

def get_current_username():
  return getpass.getuser()

def get_env_var_val(env_var):
  return os.environ.get(env_var)