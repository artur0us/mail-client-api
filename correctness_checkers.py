#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Messages correctness checkers
"""

def check_prepared_msg(prepared_msg):
  return prepared_msg

def is_msg_correct(prepared_msg):
  if "@" not in prepared_msg["from"] and "." not in prepared_msg["from"]:
    return False
  if "@" not in prepared_msg["to"] and "." not in prepared_msg["to"]:
    return False
  if prepared_msg["sent_at"] < 10000000:
    return False
  if len(prepared_msg["message_id"]) < 1:
    return False
  if len(prepared_msg["unique_hash"]) < 1:
    return False
  
  return True