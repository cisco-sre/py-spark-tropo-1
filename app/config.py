# User defined variables
# to use these in you app you must first 'from app import config',
# prefix variable names in this file with config.
# Eg, SERVER_NAME in this file would be available as config.SERVER_NAME after the import

# dCloud external URL, used when creating Spark webhook
# Public facing name of the application
SERVER_NAME = ''

# Phone number to redirect inbound voice calls to
CUSTOMER_SERVICE_REDIRECT_DN = ''

# Key for Tropo Send SMS application
TROPO_KEY = ''

# Spark token
SPARK_TOKEN = ''

# Id of Agent Team to create customer rooms under
SPARK_AGENT_TEAM_ID = ''

# Email address of Customer Proxy account - used to prevent "echo" of messages received on SMS
SPARK_CUSTOMER_PROXY_EMAIL = ''

# If set to true, agents email will need to be in the same domain as SPARK_CUSTOMER_PROXY_EMAIL
SPARK_TASK_ASSIGN_MOST_IDLE_ACTIVE = True

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
