# User defined variables
# to use these in you app you must first 'from app import config', prefix variable names in this file with config.
# Eg, SERVERNAME in this file would be availabe as config.SERVER_NAME after the import

# dCloud external URL, used when creating Spark webhook
# Public facing name of the webapp
SERVER_NAME = ''

# Phone number to redirect inbound voice calls to
CUSTOMER_SERVICE_REDIRECT_DN = ''

# Key for Tropo Send SMS application
TROPO_KEY = ''

# Spark token
SPARK_TOKEN = ''

# Id of Agent Team to create customer rooms under
SPARK_AGENT_TEAM_ID = ''
SPARK_CUSTOMERPROXY_EMAIL = ''
SPARK_TEAM_GENERAL_ROOM_ID = ''

SPARK_TASK_ASSIGN_MOST_IDLE_ACTIVE = False

# Optional: Used to validate webhook request came from Spark
SPARK_WEBHOOK_SECRET = ''

# Optional Smart Sheet integration
SMARTSHEET_TOKEN = ''

# Sheet Name
SMARTSHEET_SIGNUP_SHEET = ''

# Column Names
SMARTSHEET_COL_SIGNUP_TIME = ''
SMARTSHEET_COL_CUSTOMER_ID = ''
SMARTSHEET_COL_MESSAGE = ''
