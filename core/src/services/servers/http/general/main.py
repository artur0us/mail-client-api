from quart import Quart, request, jsonify

# Consts
from src.consts.servers.main import HTTPConsts
from src.consts.common.main import CommonConsts
from src.consts.mailbox.main import MBoxConsts
# Settings
from src.settings.mbox import MBoxSettings

from src.services.sys_entities.mailbox.parsers.parsers import MBoxParsers
from src.services.app_entities.accounts.authentication import AccountsAuthEntity

from src.services.servers.http.general.answers import Answers

class HTTPServer:

  # Main server object
  server = Quart(__name__)

  @staticmethod
  def run():
    HTTPServer.setup_router()
    HTTPServer.server.run(
      host=HTTPConsts.MAIN_HTTP_SERVER_HOST, port=HTTPConsts.MAIN_HTTP_SERVER_PORT
    )
  
  @staticmethod
  def setup_router():
    # /accounts/ routes
    @HTTPServer.server.route('/api/v1/accounts/auth/basic', methods=["GET"])
    async def qrt_acc_auth_basic():
      return jsonify(Answers.templates["NOT_IMPLEMENTED"])

    @HTTPServer.server.route('/api/v1/accounts/auth/token', methods=["GET"])
    async def qrt_acc_auth_token():
      return jsonify(Answers.templates["NOT_IMPLEMENTED"])

    @HTTPServer.server.route('/api/v1/accounts/reg/byEmail', methods=["GET"])
    async def qrt_acc_reg_by_email():
      return jsonify(Answers.templates["NOT_IMPLEMENTED"])
    
    @HTTPServer.server.route('/api/v1/mail/inbox', methods=["GET"])
    async def qrt_get_all_msgs():
      input_data = None
      try:
        input_data = await request.get_json() # {"messages": {"delete_after_receiving": true}}
      except:
        # TODO
        pass
      delete_in_final = False # Get value of this parameter from input_data variable

      if HTTPConsts.NEED_CHECK_AUTH:
        auth_token = None

        try:
          auth_token = str(request.headers['auth_token'])
        except:
          return jsonify(Answers.templates["INVALID_AUTH_TOKEN"])
        if auth_token == None or auth_token.replace(" ", "") == "": # Uncomment if you need authorization
          return jsonify(Answers.templates["INVALID_AUTH_TOKEN"])
        
        if not AccountsAuthEntity.is_authed(auth_token):
          return jsonify(Answers.templates["AUTH_ERR"])
      else:
        pass

      entityAnswer, data = MBoxParsers.get_all_msgs(MBoxSettings.USING_MBOX_FILE_PATH, delete_in_final)
      answer = Answers.render(Answers.codes["server"]["OK"], Answers.codes["request"]["OK"], entityAnswer, data, "ru")
      return jsonify(answer)
    
    @HTTPServer.server.route('/api/v1/mail/parser/oneMsg', methods=["GET"])
    async def qrt_parse_one_msg():
      if not AccountsAuthEntity.is_authed("uuid_token"):
        return jsonify(Answers.templates["AUTH_ERR"])
      """
      Input data example:
      {
          "raw_msg": "From xxxxx 2019\nSubject: Hello!\n"
      }
      """
      input_data = await request.get_json()
      entityAnswer, data = MBoxParsers.parse_one_msg(input_data["raw_msg"])
      answer = Answers.render(Answers.codes["server"]["OK"], Answers.codes["request"]["OK"], entityAnswer, data, "ru")
      return jsonify(answer)

    @HTTPServer.server.route('/api/v1/mail/attachments/oneMsg', methods=["GET"])
    async def qrt_get_one_msg_attachments():
      if not AccountsAuthEntity.is_authed("uuid_token"):
        return jsonify(Answers.templates["AUTH_ERR"])
      """
      Input data example:
      {
          "message_id": "AC1DBC0115" [PRIORITY SEARCH VARIANT]
              or
          "sent_at": "Fri 20 Oct 2019 ..."
      }
      """
      input_data = await request.get_json()
      entityAnswer, data = MBoxParsers.get_one_msg_attachments(
        sent_at=-1, message_id=input_data["message_id"]
      )
      answer = Answers.render(Answers.codes["server"]["OK"], Answers.codes["request"]["OK"], entityAnswer, data, "ru")
      return jsonify(answer)