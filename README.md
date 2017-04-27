# py-spark-tropo-1
This solution utilizes Cisco® Spark and Tropo® products API’s together with open source technologies to demonstrate a complex integration.

The goal of this lab is to focus on the integration of these products without requiring deep programming knowledge.

We will begin with a Client with a website that currently allows Customers to contact Agents by filling out a form including an email address and message. Customers will reply and send emails directly.  Agents are frustrated trying to share an inbox, customer history is tough to read as replies end up in the Agent’s email, rather than the shared mailbox.

Customers have asked that the sign-up and Agent interaction be more "mobile friendly".  They have also complained about duplication, where multiple Agents contact them about the same solution.  The Client thinks a good solution would be SMS/text, as nearly all of their customers use SMS regularly.

The Client would like to be able to organize the interactions by Customer, provide time-stamps, as well as logging the Agent name and reply. It is important that the staff does not have to install and learn “yet another program”. Recently they purchased Cisco Spark for the enterprise. Internally the staff are using Spark to collaborate from computers and mobile devices.

To accomplish the goal of modernizing the Customer interaction, the Client would like to use Cisco Spark to communicate with customers. After all, it has worked well for internal collaboration needs. The Client does not want to require Customers to sign-up and/or install an application. Any Customer requirement must be “minimal” and work for nearly all Customers with no hassle.

To solve the Client’s use-case, we will build an application that creates a new Spark Team Space (room) when a Customer first contacts the Company. An example Space name would be "2088675309".  Agents can rename the room, as long as the phone number is the last 10 characters of the name. For example “Tommy Tutone 2088675309”. By requiring the phone number in the room name, it frees us from needing a database. Each customer room provides a secure record of communication with Agents.

Team Agents receive notification of any SMS communications from the Customer.  Additionally Agents can visit the room to see past communications and if another agent is already working on the request. When an Agent sends a message to the room, the Customer receives a copy of the message via SMS. 

Agents have the feature to “whisper” to another agent in the customer’s room.  Whisper allows Agents to communicate with each other, in the context of the customer’s room, without sending the messages to the customer via SMS.

If a customer chooses to call from a voice line, forward the call to the Client’s existing Contact Center phone #. This provides a single number for voice and SMS communications.

When you have completed the following scenarios, you will have learned how to use the Cisco Spark and Tropo API’s combined with a basic Python web application to upgrade an archaic “email-only” system into a customized, real-time collaboration solution that works with web, SMS, IM and Voice! In a real world scenario, you might host the Python application on one of many cloud providers making this a server-less solution.

# Prerequisites
- git
- Python 3.6+
- pip

# First Time setup
- Clone this repository (will fail if the destination directory exists)
  * git clone https://github.com/cisco-sre/py-spark-tropo-1.git
- Enter newly created repository directory
  * cd website
- Create virtualenv
  * python virtualenv venv --python=python3
- Install requirements
  * pip install -r requirements.txt

# Launch
- From a terminal window, change to the directory where the repository was checked out above
- Make sure virtualenv is loaded
  - Mac/Linux
    * source venv/bin/activate
  - Windows
    * venv\Scripts\activate

- Set evironment variables and start flask (CTRL+C to stop)
  - Mac/Linux
    * export FLASK_DEBUG=1; export FLASK_APP=application.py; flask run
  - Windows
    * set FLASK_DEBUG=1
    * set FLASK_APP=application.py
    * flask run
    

# Notes
If you edit template files, you will need to stop and start flask to see the changes, editing python (.py) files will restart the server automatically.
