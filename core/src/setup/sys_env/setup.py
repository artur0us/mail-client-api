class SysEnvSetup:

  """
  # Setting up environment's databases, etc...
  """

  # All
  @staticmethod
  def all():
    pass
  
  # Checking for mail server, utils, transfer agent
  @staticmethod
  def check_for_mail_stuff():
    # Some checks
    return False

  # Setting up mail server, utils, transfer agent
  @staticmethod
  def setup_mail_stuff():
    if not SysEnvSetup.check_for_databases():
      # Some actions
      pass
  
  # Checking for databases
  @staticmethod
  def check_for_databases():
    # Some checks
    return False

  # Setting up databases
  @staticmethod
  def setup_databases():
    if not SysEnvSetup.check_for_databases():
      # Some actions
      pass