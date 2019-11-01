from constants import *
from sys_utils import *

def setup_all():
  global DEV_MODE
  global MAIN_MBOX_FILE_PATH

  # Main mail account username
  if not DEV_MODE:
    if "MAIL_USERNAME" in MAIN_MBOX_FILE_PATH:
      if get_env_var_val("MAIL_USERNAME") == None:
        MAIN_MBOX_FILE_PATH = MAIN_MBOX_FILE_PATH.replace("MAIL_USERNAME", get_current_username())
      else:
        if type(get_env_var_val("MAIL_USERNAME")) == str:
          MAIN_MBOX_FILE_PATH = MAIN_MBOX_FILE_PATH.replace("MAIL_USERNAME", get_env_var_val("MAIL_USERNAME"))
        else:
          exit("Error occurred while setting mail account username!")