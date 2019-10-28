#!/usr/bin/python3
# -*- coding: utf-8 -*-

from constants import *

"""
Messages drafts checkers
"""

def is_msg_draft(msg_obj):
  if not HIDE_DRAFTS:
    return True
  
  draft_chance = 0

  # Draft probability calculation
  if "mailer-daemon" in msg_obj["from"].lower():
    draft_chance = draft_chance + 1
  if "undelivered mail returned" in msg_obj["subject"].lower():
    draft_chance = draft_chance + 1
  if "this is the mail system at host" in msg_obj["body"].lower():
    draft_chance = draft_chance + 1
  
  if draft_chance > 1:
    return True
  return False