class MboxDraftsCheckers:

  @staticmethod
  def is_msg_draft(mbox_msg_obj):
    draft_chance = 0

    # Draft probability calculation
    if "mailer-daemon" in mbox_msg_obj["from"].lower():
      draft_chance = draft_chance + 1
    if "undelivered mail returned" in mbox_msg_obj["subject"].lower():
      draft_chance = draft_chance + 1
    if "this is the mail system at host" in mbox_msg_obj["body"].lower():
      draft_chance = draft_chance + 1
    
    if draft_chance > 1:
      return True
    return False