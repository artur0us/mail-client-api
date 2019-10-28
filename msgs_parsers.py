#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import mailbox
import base64
import os
import uuid
import hashlib
import html2text
from dateutil import parser as dtparser

from constants import *
from correctness_checkers import *
from msgs_parse_utils import *
from drafts_checkers import *
from spam_checkers import *

"""
Messages parsers
"""

def prepare_msg(msg_obj):
  msg_id = parse_msg_id(msg_obj["Message-ID"])
  msg_from = parse_msg_from(str(msg_obj.get_from()))
  msg_to = parse_msg_to(str(msg_obj["to"]))
  msg_subj = parse_msg_subj(msg_obj["subject"])
  msg_sent_at = int(time.mktime(
      (dtparser.parse(msg_obj["Date"])).timetuple()))

  msg_body, msg_body_charset = get_msg_body(msg_obj)
  msg_body = str(msg_body).replace("b'", "")
  if "<" in msg_body and ">" in msg_body:
      msg_body = html2text.html2text(msg_body)
  # msg_body = "Empty message body"
  # if msg_obj.is_multipart():
  #     msg_body = str(get_msg_body_new(msg_obj.get_payload()[0].get_payload(decode = True))).replace("b'", "")
  # else:
  #     msg_body = str(get_msg_body_new(msg_obj.get_payload(decode = True))).replace("b'", "")

  msg_attachments_content_types = []
  msg_attachments = []
  msg_attachments_as_base64 = []
  if "str" not in str(type(msg_obj.get_payload())):
    for idx, item in enumerate(msg_obj.get_payload()):
      if ("html" in item.get_content_type()) or ("html" in item.get_content_type()):
        # Detected body text(as attachment)
        pass
      else:
        if (item.get_filename() == None) or (item.get_filename() == "") or (item.get_filename() == " "):
          pass
        else:
          # item.get_payload(decode=True) # Returns bytes. Save this content as file(mode = wb).
          msg_attachments_as_base64.append(
            str(base64.b64encode(item.get_payload(decode=True)).decode('utf-8')))
          msg_attachments.append(item.get_filename())
      msg_attachments_content_types.append(item.get_content_type())
  else:
    msg_attachments_content_types.append(msg_obj.get_payload())

  # Formula: sha_256(str(message_id) + str(sent_at) + str(from) + str(to) + str(subject))
  msg_unique_hash = str(hashlib.sha256((
    str(msg_id) +
    str(msg_sent_at) +
    str(msg_from) +
    str(msg_to) +
    str(msg_subj)
  ).encode('utf-8')).hexdigest())

  msg = {
    "message_id": msg_id,
    "unique_hash": msg_unique_hash,
    "sent_at": msg_sent_at,
    "from": msg_from,
    "to": msg_to,
    "subject": msg_subj,
    "body": msg_body,
    "body_charset": msg_body_charset,
    "attachments_content_types": msg_attachments_content_types,
    "attachments": msg_attachments,
    "attachments_as_base64": msg_attachments_as_base64
  }

  msg = check_prepared_msg(msg)

  return msg


def get_all_msgs(mbox_file_path):
  is_err_result = False
  all_msgs = []

  try:
    mbox = mailbox.mbox(mbox_file_path)
    for idx, item in enumerate(mbox):
      prepared_msg = prepare_msg(item)
      if prepared_msg == False:
        print("[!] Current message will not be added because it has errors!")
        continue
      if not is_msg_draft(prepared_msg):
        # global all_adverts_classifier
        # if USE_SPAM_CHECKER and all_adverts_classifier != None:
        #   print(all_adverts_classifier.classify(item["body"]))
        #   all_msgs.append(prepared_msg)
        # else:
        #   all_msgs.append(prepared_msg)
        all_msgs.append(prepared_msg)
  except Exception as err:
    print("[!] Error occurred while parsing all messages!")
    print(str(err))
    is_err_result = True

  if is_err_result:
    return {
      "status": -1,
      "msg": "Error occurred while parsing all messages!",
      "data": []
    }
  return {
    "status": 1,
    "msg": "OK",
    "data": all_msgs
  }


def parse_one_msg(raw_msg):
  is_err_result = False
  tmp_mbox_filename = uuid.uuid4()
  tmp_mbox_file = open(tmp_mbox_filename, "w")
  tmp_mbox_file.write(raw_msg)
  tmp_mbox_file.close()

  prepared_msg = {}
  try:
    msg_mbox = mailbox.mbox(tmp_mbox_filename)
    prepared_msg = prepare_msg(msg_mbox[0])
  except:
    print("[!] Error occurred while parsing one message!")
    is_err_result = True

  os.remove(tmp_mbox_filename)

  if is_err_result:
    return {
      "status": -1,
      "msg": "Error occurred while parsing one message!",
      "data": {}
    }
  return {
    "status": 1,
    "msg": "OK",
    "data": prepared_msg
  }


def get_one_msg_attachments(sent_at, message_id):
  if DEV_MODE:
    all_msgs = get_all_msgs(DEV_MBOX_FILE_PATH)
  else:
    all_msgs = get_all_msgs(MAIN_MBOX_FILE_PATH)
  msg_attachments_as_base64 = []
  for idx, item in enumerate(all_msgs):
    if sent_at != None:
      if item["sent_at"] == int(sent_at):
        pass
    if item["message_id"] == str(message_id):
      msg_attachments_as_base64 = item["attachments_as_base64"]
  return {
    "status": 1,
    "message": "All attachments are received!",
    "data": msg_attachments_as_base64
  }
