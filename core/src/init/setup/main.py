# Consts
from src.consts.common.main import CommonConsts
from src.consts.mailbox.main import MBoxConsts
# Settings
from src.settings.mbox import MBoxSettings

from src.pkgs.internal.utils.sys.main import SysUtils

class Setup:

  @staticmethod
  def all():
    Setup.set_mbox_username()
  
  @staticmethod
  def set_mbox_username():
    if CommonConsts.DEV_MODE:
      MBoxSettings.USING_MBOX_FILE_PATH = MBoxConsts.LOCAL_TEST_MBOX_FILE_PATH
    else:
      MBOX_FILE_PATH = MBoxConsts.PROD_MBOX_FILE_PATH

      if MBoxConsts.MAIL_SVC_USERNAME == None:
        # Case: MAIL_SVC_USERNAME constant is not specified, so we need to get and set current system username
        MBOX_FILE_PATH = "/var/mail/" + SysUtils.get_current_username()
      elif MBoxConsts.MAIL_SVC_USERNAME.replace(" ", "") == "":
        # Case: MAIL_SVC_USERNAME constant is not specified, so we need to get and set current system username
        MBOX_FILE_PATH = "/var/mail/" + SysUtils.get_current_username()
      else:
        if not MBoxConsts.MAIL_SVC_USERNAME in MBoxConsts.PROD_MBOX_FILE_PATH:
          print("[!] Warning: mail service username is not present in mailbox file path!")
          MBOX_FILE_PATH = "/var/mail/" + MBoxConsts.MAIL_SVC_USERNAME
        else:
          MBOX_FILE_PATH = "/var/mail/" + MBoxConsts.MAIL_SVC_USERNAME
      
      MBoxSettings.USING_MBOX_FILE_PATH = MBOX_FILE_PATH