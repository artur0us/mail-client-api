class Answers:

  # Server and request codes in answer
  codes = {
    "server": {
      "UNKNOWN_ERR": -2,
      "NOT_IMPLEMENTED": -1,
      "NOTHING": 0,
      "OK": 1
    },
    "request": {
      "AUTH_ERR": -2,
      "UNKNOWN_ERR": -1,
      "NOTHING": 0,
      "OK": 1
    }
  }

  # Server and request messages in answer
  msgs = {
    "errors": {
      "AUTH_ERR": {
        "ru": "Ошибка при проверке данных авторизации!",
        "en": "Error verifying authorization data!"
      },
      "UNKNOWN_ERR": {
        "ru": "Неизвестная ошибка!",
        "en": "Unknown error!"
      },
      "NOT_IMPLEMENTED": {
        "ru": "Данная возможность ещё не реализована!",
        "en": "This feature has not yet been implemented!"
      }
    },
    "warnings": {
      
    },
    "ok": {
      "ALL_OK": {
        "ru": "ОК",
        "en": "OK"
      }
    }
  }
  
  # Full answers templates
  templates = {
    "INVALID_AUTH_TOKEN": {
      "ok": False,
      "server_code": codes["server"]["OK"],
      "request_code": codes["request"]["AUTH_ERR"],
      "entitiy_code": 0,
      "msg": "Invalid auth token",
      "data": {}
    },
    "AUTH_ERR": {
      "ok": False,
      "server_code": codes["server"]["OK"],
      "request_code": codes["request"]["AUTH_ERR"],
      "entitiy_code": 0,
      "msg": "Authentication error! Check your credentials!",
      "data": {}
    },
    "NOT_IMPLEMENTED": {
      "ok": False,
      "server_code": codes["server"]["NOT_IMPLEMENTED"],
      "request_code": codes["request"]["NOTHING"],
      "entitiy_code": 0,
      "msg": "This HTTP method is not implemented!",
      "data": {}
    },
    "DEFAULT": {
      "ok": True,
      "server_code": codes["server"]["NOTHING"],
      "request_code": codes["request"]["NOTHING"],
      "entitiy_code": 0,
      "msg": "OK",
      "data": {}
    }
  }

  @staticmethod
  def render(serverCode, requestCode, entityAnswer, data, lang):
    # Preparing template
    renderedAnswer = Answers.templates["DEFAULT"]

    # Preparing codes
    renderedAnswer["server_code"] = serverCode
    renderedAnswer["request_code"] = requestCode
    renderedAnswer["entitiy_code"] = entityAnswer["code"]

    # Preparing messages
    if entityAnswer["msg"][lang].replace(" ", "") == "":
      renderedAnswer["msg"] = renderedAnswer["msg"]
    else:
      renderedAnswer["msg"] = entityAnswer["msg"][lang]
    
    # Preparing data
    renderedAnswer["data"] = data

    # Preparing final result flag
    renderedAnswer["ok"] = True
    if renderedAnswer["server_code"] < 0 or renderedAnswer["request_code"] < 0 or renderedAnswer["entitiy_code"] < 0:
      renderedAnswer["ok"] = False
    
    return renderedAnswer