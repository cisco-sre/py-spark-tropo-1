# demo-site 

# Prerequisites
- git
- Python 3.6+
- pip

# First Time setup
- Clone this repository (will fail if the destination directory exists)
  * git clone https://github.com/rsp2k/website.git
- Enter newly created repository directory
  * cd website
- Create virtualenv
  * python virtualenv venv --python=python3
- Install requirements
  * pip install -r requirements.txt
- Edit .env file
  * TROPO_TOKEN
  * SPARK_TOKEN
  * SPARK_AGENT_TEAM_ID
  - For optional SmartSheet integraton
    * SMARTSHEET_TOKEN
    * SMARTSHEET_SIGNUP_SHEET

# Launch
- From a terminal window, change to the directory where the repository was checked out above
- Make sure virtualenv is loaded
  - Mac/Linux
    * source venv/bin/activate
  - Windows
    * venv\Scripts\activate

* Start flask
flask --app app

# Notes
If you edit template files, you will need to stop and start flask to see the changes, editing python (.py) files will restart the server automatically.
