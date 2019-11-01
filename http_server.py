from quart import Quart, request, jsonify

from constants import *
from msgs_parsers import *
from auth import *

"""
HTTP Server
"""
# Server app
qrt_app = Quart(__name__)

# Answers templates
answers_templates = {
  "auth_err": {
    "server_status": 1,
    "status": -1,
    "msg": "Authentication error! Check your credentials!",
    "data": {}
  },
  "not_implemented": {
    "server_status": -1,
    "status": 0,
    "msg": "This HTTP method is not implemented!",
    "data": {}
  }
}

# Routes
@qrt_app.route('/api/v1/accounts/auth/basic', methods=["GET"])
async def qrt_acc_auth_basic():
  return jsonify(answers_templates["not_implemented"])

@qrt_app.route('/api/v1/accounts/auth/token', methods=["GET"])
async def qrt_acc_auth_token():
  return jsonify(answers_templates["not_implemented"])

@qrt_app.route('/api/v1/accounts/reg/byEmail', methods=["GET"])
async def qrt_acc_reg_by_email():
  return jsonify(answers_templates["not_implemented"])

@qrt_app.route('/api/v1/mail/inbox', methods=["GET"])
async def qrt_get_all_msgs():
  if not is_authed("uuid_token"):
    return jsonify(answers_templates["auth_err"])
  if DEV_MODE:
    all_msgs = get_all_msgs(DEV_MBOX_FILE_PATH)
  else:
    all_msgs = get_all_msgs(MAIN_MBOX_FILE_PATH)
  return jsonify(all_msgs)


@qrt_app.route('/api/v1/mail/parser/oneMsg', methods=["GET"])
async def qrt_parse_one_msg():
  if not is_authed("uuid_token"):
    return jsonify(answers_templates["auth_err"])
  """
  Input data example:
  {
      "raw_msg": "From xxxxx 2019\nSubject: Hello!\n"
  }
  """
  input_data = await request.get_json()
  msg = parse_one_msg(input_data["raw_msg"])
  return jsonify(msg)


@qrt_app.route('/api/v1/mail/attachments/oneMsg', methods=["GET"])
async def qrt_get_one_msg_attachments():
  if not is_authed("uuid_token"):
    return jsonify(answers_templates["auth_err"])
  """
  Input data example:
  {
      "message_id": "AC1DBC0115" [PRIORITY SEARCH VARIANT]
          or
      "sent_at": "Fri 20 Oct 2019 ..."
  }
  """
  input_data = await request.get_json()
  one_msg_attachments = get_one_msg_attachments(
      sent_at=-1, message_id=input_data["message_id"])
  return jsonify(one_msg_attachments)

# Another functions
def run_http():
  qrt_app.run(host=HTTP_SERVER_HOST, port=HTTP_SERVER_PORT)