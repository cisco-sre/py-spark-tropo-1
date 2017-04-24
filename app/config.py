# User defined variables
# to use these in you app you must first 'from app import config', prefix variable names in this file with config.
# Eg, SERVERNAME in this file would be availabe as config.SERVER_NAME after the import

# dCloud external URL, used when creating Spark webhook
# Public facing name of the webapp
SERVER_NAME = 'webapp.vpod651.dc-01.com'

# Phone number to redirect inbound voice calls to
CUSTOMER_SERVICE_REDIRECT_DN = '+12083756499'

# Key for Tropo Send SMS application
TROPO_KEY = '69554e5a6d6e5a6a4371766e465a43526255547543536a4463486d684d5265764a6e754675796a6d6f6c536f'

# Spark token
SPARK_TOKEN = 'M2Q2ZjYxZGMtMWVkNy00M2ZjLWI3ZWMtZGEzMWI0NWMwZDUzOGM4NjJlMjYtYWMw'

# Id of Agent Team to create customer rooms under
SPARK_AGENT_TEAM_ID = '9bbab210-2637-11e7-a892-e9d58302014a'
SPARK_CUSTOMER_EMAIL = 'kkdoijvr@sharklasers.com'
SPARK_TEAM_GENERAL_ROOM_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vYTlkNzkwNDAtMjYwOC0xMWU3LWIyZmEtZmI4YzMyNmRkMzI0'

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
