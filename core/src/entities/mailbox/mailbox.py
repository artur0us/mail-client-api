import mailbox, time, sys, traceback

class MBoxEntity:

  is_mbox_locked = False

  @staticmethod
  def change_username(new_username):
    pass
  
  @staticmethod
  def delete_messages_by_keys(mbox_file_path, msgs_keys_to_delete):
    if type(mbox_file_path) != str:
      return False
    if len(mbox_file_path) < 1:
      return False
    if type(msgs_keys_to_delete) != list:
      return False
    
    MBoxEntity.is_mbox_locked = True
    print("Deleting messages(count: " + str(len(msgs_keys_to_delete)) + ")...")
    time.sleep(5) # Simulated delay

    mbox = mailbox.mbox(mbox_file_path)
    mbox.lock()
    try:
      for one_msg_key in msgs_keys_to_delete:
        mbox.remove(one_msg_key)
    except:
      print("Error occurred while deleting messages! Traceback:")
      traceback.print_exc()
      exc_type, exc_value, exc_traceback = sys.exc_info()
      traceback_info = traceback.format_tb(exc_traceback)
      print(traceback_info)
      MBoxEntity.is_mbox_locked = False
    finally:
      mbox.flush()
      mbox.close()
      MBoxEntity.is_mbox_locked = False
    
    MBoxEntity.is_mbox_locked = False

    print("Messages successfully deleted!")

    return True