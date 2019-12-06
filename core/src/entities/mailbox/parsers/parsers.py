import os, uuid, chardet, email.header, time, base64, hashlib, mailbox, threading

import html2text
from dateutil import parser as dtparser

from src.consts.app.consts import AppConsts
from src.consts.mailbox.consts import MBoxConsts

from src.entities.mailbox.checkers.correctness.checkers import MBoxCorrectCheckersEntity
from src.entities.mailbox.checkers.drafts.checkers import MboxDraftsCheckers
from src.entities.mailbox.checkers.spam.checkers import MBoxSpamCheckers

from src.entities.mailbox.mailbox import MBoxEntity

class MBoxParsers:

  @staticmethod
  def prepare_msg(msg_obj):
    msg_id = MBoxParsers.parse_msg_id(msg_obj["Message-ID"])
    msg_from = MBoxParsers.parse_msg_from(str(msg_obj.get_from()))
    msg_to = MBoxParsers.parse_msg_to(str(msg_obj["to"]))
    msg_subj = MBoxParsers.parse_msg_subj(msg_obj["subject"])
    msg_sent_at = int(time.mktime(
        (dtparser.parse(msg_obj["Date"])).timetuple()))

    msg_body, msg_body_charset = MBoxParsers.get_msg_body(msg_obj)
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
    if str(type(msg_obj.get_payload())) != str:
      for idx, item in enumerate(msg_obj.get_payload()):
        try:
          item.get_content_type()
        except:
          continue
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

    msg = MBoxCorrectCheckersEntity.check_prepared_msg(msg)

    return msg


  @staticmethod
  def get_all_msgs(mbox_file_path, delete_in_final):
    is_err_result = False
    all_msgs = []
    msgs_keys_to_delete = []
    
    if MBoxEntity.is_mbox_locked:
      return {
        "status": -2,
        "msg": "Service is busy!",
        "data": []
      }

    mbox = None
    try:
      mbox = mailbox.mbox(mbox_file_path)
      for idx, item in mbox.iteritems(): # Old: for idx, item in enumerate(mbox):
        prepared_msg = MBoxParsers.prepare_msg(item)
        if prepared_msg == False:
          print("[!] Current message will not be added because it has errors!")
          continue
        if not MboxDraftsCheckers.is_msg_draft(prepared_msg):
          msg_can_be_added = True
          
          if not MBoxCorrectCheckersEntity.is_msg_correct(prepared_msg):
            print("[!] Current message is not correct!")
            msg_can_be_added = False
          if MBoxConsts.USE_SPAM_CHECKER and MBoxSpamCheckers.adverts_classifier != None:
            if MBoxSpamCheckers.adverts_classifier.classify(prepared_msg["body"])[0][1] > 0.55:
              print("[!] Current message is advertisement!")
              msg_can_be_added = False
          
          if msg_can_be_added:
            all_msgs.append(prepared_msg)
          
          msgs_keys_to_delete.append(idx)
    except Exception as err:
      print("[!] Error occurred while parsing all messages!")
      print(str(err))
      is_err_result = True
    
    if mbox != None:
      mbox.unlock()
      mbox.close()
    
    if (
      (not is_err_result)
      and (delete_in_final)
      and (mbox != None)
      and (not MBoxEntity.is_mbox_locked)
    ):
      # Delete messages
      pass
      threading.Thread(target=MBoxEntity.delete_messages_by_keys, args=(mbox_file_path, msgs_keys_to_delete, )).start()
 
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


  @staticmethod
  def parse_one_msg(raw_msg):
    is_err_result = False
    tmp_mbox_filename = uuid.uuid4()
    tmp_mbox_file = open(tmp_mbox_filename, "w")
    tmp_mbox_file.write(raw_msg)
    tmp_mbox_file.close()

    prepared_msg = {}
    try:
      msg_mbox = mailbox.mbox(tmp_mbox_filename)
      prepared_msg = MBoxParsers.prepare_msg(msg_mbox[0])
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


  @staticmethod
  def get_one_msg_attachments(sent_at, message_id):
    if AppConsts.DEV_MODE:
      all_msgs = MBoxParsers.get_all_msgs(MBoxConsts.DEV_MBOX_FILE_PATH)
    else:
      all_msgs = MBoxParsers.get_all_msgs(MBoxConsts.MAIN_MBOX_FILE_PATH)
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
  
  ######################################################
  ######################################################
  ######################################################
  ######################################################
  ######################################################

  @staticmethod
  def get_msg_charsets(msg_obj):
    charsets = set({})
    for c in msg_obj.get_charsets():
      if c is not None:
        charsets.update([c])
    return charsets


  @staticmethod
  def get_msg_body(msg_obj):
    while msg_obj.is_multipart():
      msg_obj = msg_obj.get_payload()[0]
    t = msg_obj.get_payload(decode=True)
    # print(t)
    using_charset = "utf-8"
    for charset in MBoxParsers.get_msg_charsets(msg_obj):
      # print(charset)
      t = t.decode(charset)
      using_charset = charset
    return t, using_charset


  @staticmethod
  def get_msg_body_new(msg_body_content):
    for charset in MBoxParsers.get_msg_charsets(msg_body_content):
      msg_body_content = msg_body_content.decode(charset)
    return msg_body_content


  @staticmethod
  def parse_msg_id(msg_id):
    msg_id = str(msg_id)
    msg_id = msg_id.replace("<", "").replace(">", "")
    if " " in msg_id:
      splitted_msg_id = msg_id.split(" ")
      for idx, item in enumerate(splitted_msg_id):
        if ("@" in str(item)) and ("." in str(item)):
          pass
        else:
          msg_id = str(item)
          break
    elif ("@" in msg_id) and ("." in msg_id):
      msg_id = msg_id.split("@")[0]
    return msg_id


  @staticmethod
  def parse_msg_from(msg_from):
    splitted_msg_from = msg_from.split(" ")
    if len(splitted_msg_from) > 0:
      for idx, item in enumerate(splitted_msg_from):
        if ("@" in item) and ("." in item):
          msg_from = item
          break
    msg_from = msg_from.replace('\"', "").replace('<', "").replace('>', "")
    return msg_from


  @staticmethod
  def parse_msg_to(msg_to):
      splitted_msg_to = msg_to.split(" ")
      if len(splitted_msg_to) > 0:
        for idx, item in enumerate(splitted_msg_to):
          if ("@" in item) and ("." in item):
            msg_to = item
            break
      msg_to = msg_to.replace('\"', "").replace('<', "").replace('>', "")
      return msg_to


  @staticmethod
  def parse_msg_subj(msg_subj):
    msg_subj_encoding = "utf-8"
    # msg_subj = "Unknown message subject"
    # msg_subj = (email.header.decode_header(msg_subj)[0][1])

    # Message subject could be empty or invalid
    if msg_subj == None:
      return "Empty or invalid subject"

    # Checking message's subject for None
    # TODO: remove this actions
    if msg_subj == None:
      msg_subj = (email.header.decode_header(msg_subj)[0][0])
    if msg_subj == None:
      msg_subj = (email.header.decode_header(msg_subj)[0])
    if msg_subj == None:
      msg_subj = (email.header.decode_header(msg_subj)[1])

    # Checking message's subject for incorrect value(now for encoding)
    encoding_variants = [
      {
        "name": "utf-8",
        "variants": [
          "utf-8", "utf8", "utf 8", "utf_8",
        ]
      },
      {
        "name": "utf-16-le",
        "variants": [
          "utf-16-le", "utf 16 le", "utf-16 le", "utf 16-le", "utf_16_le"
        ]
      },
      {
        "name": "cp1251",
        "variants": [
          "cp1251", "cp_1251", "1251"
        ]
      },
      {
        "name": "koi8-r",
        "variants": [
          "koi8-r", "koi8 r", "koi8_r"
        ]
      },
      {
        "name": "koi8-u",
        "variants": [
          "koi8-u", "koi8 u", "koi8_u"
        ]
      },
      {
        "name": "iso-8859-1",
        "variants": [
          "iso-8859-1", "iso 8859 1", "iso-8859 1", "iso 8859-1", "iso_8859_1"
        ]
      },
    ]
    for idx, item in enumerate(encoding_variants):
      for idx2, item2 in enumerate(item["variants"]):
        if item2 in str(msg_subj.lower()):
          msg_subj = (email.header.decode_header(msg_subj)[0][0])
          msg_subj_encoding = item["name"]
          if item2 in str(msg_subj.lower()):
            msg_subj = (email.header.decode_header(msg_subj)[0][1])
            msg_subj_encoding = item["name"]
          if item2 in str(msg_subj.lower()):
            msg_subj = (email.header.decode_header(msg_subj)[0])
            msg_subj_encoding = item["name"]
          if item2 in str(msg_subj.lower()):
            msg_subj = (email.header.decode_header(msg_subj))
            msg_subj_encoding = item["name"]

    # Checking message's subject for None again(for wtf situation)
    # TODO: remove this actions
    if msg_subj == None:
      msg_subj = (email.header.decode_header(msg_subj)[0][0])
    if msg_subj == None:
      msg_subj = (email.header.decode_header(msg_subj)[0])
    if msg_subj == None:
      msg_subj = (email.header.decode_header(msg_subj)[1])

    # msg_subj = msg_subj.decode(chardet.detect(msg_subj))
    if str(type(msg_subj)) == bytes:
      msg_subj = str(msg_subj.decode(msg_subj_encoding))

    msg_subj = msg_subj.replace('\"', "")
    return msg_subj