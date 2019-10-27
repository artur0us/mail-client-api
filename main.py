from quart import Quart, request, jsonify

from constants import *
from msgs_parsers import *

"""
HTTP Server
"""
# Server app
qrt_app = Quart(__name__)

# Routes
@qrt_app.route('/api/v1/mail/inbox', methods=["GET"])
async def qrt_get_all_msgs():
    all_msgs = get_all_msgs(MAIN_MBOX_FILE_PATH)
    return jsonify(all_msgs)

@qrt_app.route('/api/v1/mail/parser/oneMsg', methods=["GET"])
async def qrt_parse_one_msg():
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
    """
    Input data example:
    {
        "message_id": "AC1DBC0115" [PRIORITY SEARCH VARIANT]
            or
        "sent_at": "Fri 20 Oct 2019 ..."
    }
    """
    input_data = await request.get_json()
    one_msg_attachments = get_one_msg_attachments(sent_at = -1, message_id = input_data["message_id"])
    return jsonify(one_msg_attachments)

"""
App entry point
"""
def main():
    qrt_app.run(host="0.0.0.0", port=12004)

main()