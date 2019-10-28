#!/usr/bin/python3
# -*- coding: utf-8 -*-

import email.header
import chardet

"""
Messages parse utils
"""

def get_msg_charsets(msg_obj):
  charsets = set({})
  for c in msg_obj.get_charsets():
    if c is not None:
      charsets.update([c])
  return charsets


def get_msg_body(msg_obj):
  while msg_obj.is_multipart():
    msg_obj = msg_obj.get_payload()[0]
  t = msg_obj.get_payload(decode=True)
  # print(t)
  using_charset = "utf-8"
  for charset in get_msg_charsets(msg_obj):
    # print(charset)
    t = t.decode(charset)
    using_charset = charset
  return t, using_charset


def get_msg_body_new(msg_body_content):
  for charset in get_msg_charsets(msg_body_content):
    msg_body_content = msg_body_content.decode(charset)
  return msg_body_content


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


def parse_msg_from(msg_from):
  splitted_msg_from = msg_from.split(" ")
  if len(splitted_msg_from) > 0:
    for idx, item in enumerate(splitted_msg_from):
      if ("@" in item) and ("." in item):
        msg_from = item
        break
  msg_from = msg_from.replace('\"', "").replace('<', "").replace('>', "")
  return msg_from


def parse_msg_to(msg_to):
    splitted_msg_to = msg_to.split(" ")
    if len(splitted_msg_to) > 0:
      for idx, item in enumerate(splitted_msg_to):
        if ("@" in item) and ("." in item):
          msg_to = item
          break
    msg_to = msg_to.replace('\"', "").replace('<', "").replace('>', "")
    return msg_to


def parse_msg_subj(msg_subj):
  msg_subj_encoding = "utf-8"
  # msg_subj = "Unknown message subject"
  # msg_subj = (email.header.decode_header(msg_subj)[0][1])

  # Checking message's subject for None
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
  if msg_subj == None:
    msg_subj = (email.header.decode_header(msg_subj)[0][0])
  if msg_subj == None:
    msg_subj = (email.header.decode_header(msg_subj)[0])
  if msg_subj == None:
    msg_subj = (email.header.decode_header(msg_subj)[1])

  # msg_subj = msg_subj.decode(chardet.detect(msg_subj))
  if "byte" in str(type(msg_subj)):
    msg_subj = str(msg_subj.decode(msg_subj_encoding))

  msg_subj = msg_subj.replace('\"', "")
  return msg_subj
