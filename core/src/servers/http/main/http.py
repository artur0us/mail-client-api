from quart import Quart, request, jsonify

from src.consts.servers.http.consts import HTTPConsts
from src.consts.app.consts import AppConsts
from src.consts.mailbox.consts import MBoxConsts

from src.entities.mailbox.parsers.parsers import MBoxParsers
from src.entities.accounts.app.authentication.authentication import AccountsAuthEntity

class MainHTTPServer:

  # Main server object
  server = Quart(__name__)

  # Server answers templates
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

  @staticmethod
  def run():
    MainHTTPServer.setup_router()
    MainHTTPServer.server.run(
      host=HTTPConsts.MAIN_HTTP_SERVER_HOST, port=HTTPConsts.MAIN_HTTP_SERVER_PORT
    )
  
  @staticmethod
  def setup_router():
    # /accounts/ routes
    @MainHTTPServer.server.route('/api/v1/accounts/auth/basic', methods=["GET"])
    async def qrt_acc_auth_basic():
      return jsonify(MainHTTPServer.answers_templates["not_implemented"])

    @MainHTTPServer.server.route('/api/v1/accounts/auth/token', methods=["GET"])
    async def qrt_acc_auth_token():
      return jsonify(MainHTTPServer.answers_templates["not_implemented"])

    @MainHTTPServer.server.route('/api/v1/accounts/reg/byEmail', methods=["GET"])
    async def qrt_acc_reg_by_email():
      return jsonify(MainHTTPServer.answers_templates["not_implemented"])
    
    @MainHTTPServer.server.route('/api/v1/mail/inbox', methods=["GET"])
    async def qrt_get_all_msgs():
      if not AccountsAuthEntity.is_authed("uuid_token"):
        return jsonify(MainHTTPServer.answers_templates["auth_err"])
      if AppConsts.DEV_MODE:
        all_msgs = MBoxParsers.get_all_msgs(MBoxConsts.DEV_MBOX_FILE_PATH)
      else:
        all_msgs = MBoxParsers.get_all_msgs(MBoxConsts.MAIN_MBOX_FILE_PATH)
      return jsonify(all_msgs)
    
    @MainHTTPServer.server.route('/api/v1/mail/parser/oneMsg', methods=["GET"])
    async def qrt_parse_one_msg():
      if not AccountsAuthEntity.is_authed("uuid_token"):
        return jsonify(MainHTTPServer.answers_templates["auth_err"])
      """
      Input data example:
      {
          "raw_msg": "From xxxxx 2019\nSubject: Hello!\n"
      }
      """
      input_data = await request.get_json()
      msg = MBoxParsers.parse_one_msg(input_data["raw_msg"])
      return jsonify(msg)

    @MainHTTPServer.server.route('/api/v1/mail/attachments/oneMsg', methods=["GET"])
    async def qrt_get_one_msg_attachments():
      if not AccountsAuthEntity.is_authed("uuid_token"):
        return jsonify(MainHTTPServer.answers_templates["auth_err"])
      """
      Input data example:
      {
          "message_id": "AC1DBC0115" [PRIORITY SEARCH VARIANT]
              or
          "sent_at": "Fri 20 Oct 2019 ..."
      }
      """
      input_data = await request.get_json()
      one_msg_attachments = MBoxParsers.get_one_msg_attachments(
          sent_at=-1, message_id=input_data["message_id"])
      return jsonify(one_msg_attachments)