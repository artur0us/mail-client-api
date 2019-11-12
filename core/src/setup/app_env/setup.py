from src.consts.app.consts import AppConsts
from src.consts.mailbox.consts import MBoxConsts

from src.utils.sys.utils import SysUtils

class AppEnvSetup:

  """
  # Setting up application's some stuff
  """

  # All
  @staticmethod
  def all():
    AppEnvSetup.mailbox_username()

  # Setting mailbox username which will be used
  @staticmethod
  def mailbox_username():
    if not AppConsts.DEV_MODE:
      if "MAIL_USERNAME" in MBoxConsts.MAIN_MBOX_FILE_PATH:
        if SysUtils.get_env_var_val("MAIL_USERNAME") == None:
          MBoxConsts.MAIN_MBOX_FILE_PATH = MBoxConsts.MAIN_MBOX_FILE_PATH.replace("MAIL_USERNAME", SysUtils.get_current_username())
        else:
          if type(SysUtils.get_env_var_val("MAIL_USERNAME")) == str:
            MBoxConsts.MAIN_MBOX_FILE_PATH = MBoxConsts.MAIN_MBOX_FILE_PATH.replace("MAIL_USERNAME", SysUtils.get_env_var_val("MAIL_USERNAME"))
          else:
            exit("Error occurred while setting mail account username!")