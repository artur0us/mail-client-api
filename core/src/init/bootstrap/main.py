# Consts
from src.consts.common.main import CommonConsts
from src.consts.mailbox.main import MBoxConsts
# Settings
from src.settings.mbox import MBoxSettings

from src.services.servers.http.general.main import HTTPServer

class Bootstrap:

  @staticmethod
  def all():
    HTTPServer.run()