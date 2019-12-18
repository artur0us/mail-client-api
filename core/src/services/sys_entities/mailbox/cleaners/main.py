import mailbox, time, sys, traceback, os
from datetime import datetime, date #, time
from shutil import copyfile

# Consts
from src.consts.common.main import CommonConsts
from src.consts.mailbox.main import MBoxConsts
# Settings
from src.settings.mbox import MBoxSettings

from src.services.sys_entities.mailbox.mailbox import MBoxEntity

class MBoxCleaners:
  
  @staticmethod
  def delete_messages_by_keys(mbox_file_path, msgs_keys_to_delete):
    # Waiting for mailbox file unlock
    mboxUnlockWaitAttempts = 0
    mboxUnlockWaitMaxAttempts = 100
    while MBoxEntity.is_mbox_locked:
      print("[i] Waiting for mailbox unlock before unnecessary messages removal...")
      if mboxUnlockWaitAttempts > mboxUnlockWaitMaxAttempts:
        print("[!] Unnecessary messages removal method timeout! Attempts count: " + str(mboxUnlockWaitAttempts))
        return False
      mboxUnlockWaitAttempts = mboxUnlockWaitAttempts + 1
      time.sleep(5)
    
    if type(mbox_file_path) != str:
      return False
    if len(mbox_file_path) < 1:
      return False
    if type(msgs_keys_to_delete) != list:
      return False
    
    MBoxEntity.is_mbox_locked = True
    print("Deleting messages(count: " + str(len(msgs_keys_to_delete)) + ")...")
    time.sleep(2) # Simulated delay

    # TODO: backup mailbox file
    now = datetime.now()
    copyfile(MBoxSettings.USING_MBOX_FILE_PATH, "data/backups/mailbox_backup__" + str(now.strftime("%d%m%Y_%I%M%S")))
    
    # TODO: remove old mailbox backups

    mbox = mailbox.mbox(mbox_file_path)
    mbox.lock()
    try:
      for one_msg_key in msgs_keys_to_delete:
        mbox.remove(one_msg_key)
    except:
      print("Error occurred while deleting messages! Traceback:")
      # traceback.print_exc() # TODO: remove this line
      exc_type, exc_value, exc_traceback = sys.exc_info()
      traceback_info = traceback.format_tb(exc_traceback)
      print(traceback_info)
      MBoxEntity.is_mbox_locked = False
    finally:
      mbox.flush()
      mbox.close()
      MBoxEntity.is_mbox_locked = False

    # chown <MAIL_USERNAME> /var/mail/<MAIL_USERNAME>  // As administrator/superuser(sudo)
    os.system("chown " + MBoxConsts.MAIL_SVC_USERNAME + " " + MBoxSettings.USING_MBOX_FILE_PATH)
    
    MBoxEntity.is_mbox_locked = False

    print("Messages successfully deleted!")

    return True