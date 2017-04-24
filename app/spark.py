import hashlib
import hmac
import random
import logging

from flask import abort

import ciscosparkapi

from app import config
from app import tropo


def create_new_message_webhook(room, webhook_url):
    """
    Create the webhook if it doesn't already exist. The Webhook is triggered when new messages are posted to the room.
    :param room: Cisco Spark Room object to create webhook in 
    :param webhook_url: URL for webhook to POST JSON payload to
    :return: Cisco Spark Webhook object.
    """
    # when  a message
    resource = "messages"
    # is created
    event = "created"
    filter_ = ""

    # insecure example secret used to generate the payload signature
    secret = config.SPARK_WEBHOOK_SECRET

    # Connect to SparkAPI with SPARK_TOKEN
    spark_api = ciscosparkapi.CiscoSparkAPI(access_token=config.SPARK_TOKEN)

    webhook_name = 'messages created'
    # search webhooks items for matching
    for webhook in spark_api.webhooks.list():
        if webhook.name == webhook_name:
            break
    else:
        webhook = spark_api.webhooks.create(webhook_name,
            webhook_url, resource, event, filter_, secret)

    return webhook


def assign_team_member_to_customer_room(room, **room_args):
    """
    Find an active agent on the team and assign them to the room
    :param room: Spark API room object to assign a team member to
    :param room_args: message that was posted to room
    :return: True if agent is assigned or False
    """

    logging.log(logging.INFO, 'assign_team_member_to_customer_room')

    # setup Spark API connection using SPARK_TOKEN
    spark_api = ciscosparkapi.CiscoSparkAPI(access_token=config.SPARK_TOKEN)

    person_ids_in_room = []
    logging.log(logging.INFO, room)

    # Who is already in the room
    for membership in spark_api.memberships.list(roomId=room.id):
        person_ids_in_room.append(membership.personId)

    available_people = []
    # Loop over all members of team
    for membership in spark_api.team_memberships.list(teamId=config.SPARK_AGENT_TEAM_ID):

        # Skip people already in room
        if membership.personId in person_ids_in_room:
            continue

        # Get the person object for current membership
        person = spark_api.people.get(membership.personId)

        # NOTE: Status is only shown to users in the same domain!
        if person.status == 'active':
            available_people.append(person)

    logging.log(logging.INFO, 'Available people %s' % available_people)
    # If no agents are active, we cant assign one
    if not available_people:
        return False

    # Get the most idle, available user
    if config.SPARK_TASK_ASSIGN_MOST_IDLE_ACTIVE:
        available_people.sort(key=lambda agent: agent.lastActivity, reverse=True)
    else:
        # Random agent
        random.shuffle(available_people)

    agent_to_assign = available_people.pop()

    logging.log(logging.INFO, 'Assiging %s' % agent_to_assign)
    # assign agent to room
    membership = spark_api.memberships.create(room.id, personId=agent_to_assign.id)

    if membership:
        # indicate success
        return True

    # in case of failure assigning agent to room
    return False


def customer_room_message_send(customer_id, **room_args):
    """
    Posts message to customer's Spark Room for customer_id using room_args. Room/Webhook will be created if necessary.
    :param customer_id: Customer Phone Number (may start with 1)
    :param room_args: text/markup/file/webhook_url
    :return: Cisco Spark Message object 
    """

    # Basic sanity checking
    if 'text' not in room_args and 'markup' not in room_args and 'files' not in room_args:
        raise PassedParametersError("Must specify at least one of text/markup/files")

    # setup Spark API connection using SPARK_TOKEN
    spark_api = ciscosparkapi.CiscoSparkAPI(access_token=config.SPARK_TOKEN)

    # loop through rooms for SPARK_AGENT_TEAM_ID, looking for customer room
    for room in spark_api.rooms.list(teamId=config.SPARK_AGENT_TEAM_ID):
        # Compare first 10 characters of each
        if is_customers_room(room, customer_id):
            break # stop looping if we found the customers room

    # If room is not found and break is never encountered, else block runs
    # http://book.pythontips.com/en/latest/for_-_else.html
    else:
        # New customer
        room = customer_new_signup(spark_api, customer_id, config.SPARK_AGENT_TEAM_ID, room_args['text'], room_args['webhook_url'])

    # Check if any agents are in the room
    for membership in spark_api.memberships.list(roomId=room.id):
        if membership.personEmail == config.SPARK_CUSTOMER_EMAIL:
            # Skip our "bot user"
            logging.log(logging.INFO, 'Skipping bot user')
            continue

        # Fetch person object from Spark API
        person = spark_api.people.get(membership.personId)

        # https://developer.ciscospark.com/blog/blog-details-8727.html
        if person.status == 'active':
            logging.log(logging.INFO, 'Found active person %s' % person)
            # Agent is in the room and active, count on them to handle reqeust
            break
    else:
        # No agents are in room that are active, assign one from the team
        agent_assigned = assign_team_member_to_customer_room(room, **room_args)

        if not agent_assigned:
            message_to_customer = "No agents are available at the moment. We will assist you as soon as we can."
            tropo.send_sms(customer_id, message_to_customer)

            message_to_team = "Customer Waiting in room: %s" % customer_id

            # Find general room by sorting by created date
            team_rooms = sorted(spark_api.rooms.list(teamId=config.SPARK_AGENT_TEAM_ID),
                                key=lambda room: room.created,
                                reverse=True)

            # pop the oldest room from the list
            team_room = team_rooms.pop()

            spark_api.messages.create(roomId=team_room.id, text=message_to_team)

    # remove webhook url since spark API doesn't accept it
    del(room_args['webhook_url'])
    # post the message to spark room
    return spark_api.messages.create(roomId=room.id, **room_args)


class PassedParametersError(Exception):
    pass


def is_customers_room(room, customer_id):
    """
    Check if given room belongs to customer_id. Looks at last 10 characters of each
    :param room: Spark Room Object
    :param customer_id: Customer Phone Number (may start with 1)
    :return: True or False
    """
    room_last_10 = room.title[-10:]
    customer_id_last10 = customer_id[-10:]
    if room_last_10 == customer_id_last10:
        return True
    logging.log(logging.INFO, "NO MATCH", room_last_10, customer_id_last10)
    return False


def customer_new_signup(spark_api, customer_id, team_id, message_from_customer, webhook_url):
    """
    Create room/webhook and post message room then send customer SMS
    :param spark_api: Cisco Spark API Object
    :param customer_id: Customer Phone Number (may start with 1)
    :param team_id: Team ID to create Customer Room under
    :param message_from_customer: Text of message sent from customer when they signed up
    :param webhook_url: URL to use when creating webhook
    :return: Cisco Spark Room objecct
    """

    # Send message via tropo
    message = "Thanks for signing up! To get in touch, reply to this message or call this number during business hours."
    tropo.send_sms(customer_id[-10:], message)

    # Fetch all rooms and loop over them
    for room in spark_api.rooms.list():
        if is_customers_room(room, customer_id):
            # If customer room is found we are done
            break
    else:
        # no room exists for customer, create a new team room
        # http://ciscosparkapi.readthedocs.io/en/latest/user/api.html#ciscosparkapi.RoomsAPI.create
        room = spark_api.rooms.create(customer_id, teamId=team_id)

    # create webhook if needed
    # http://ciscosparkapi.readthedocs.io/en/latest/user/api.html#ciscosparkapi.WebhooksAPI.create
    webhook = create_new_message_webhook(room, webhook_url)

    # OPTIONALLY CALL SMARTSHEET IF VARS ARE FILLED OUT IN app/config.py
    # from app.smartsheet_log import smartsheet_log_signup
    # smartsheet_log_signup(customer_id, datetime.now(), message_from_customer)

    return room


def webhook_process(request):
    """
    Send any room messages to customer by SMS, making sure not to echo customer's SMS or @mention messages.
    :param request: Flask request object
    :return: Flask response
    """

    # Basic sanity checking
    if not request.json or not ('event' in request.json and 'data' in request.json):
        logging.log(logging.ERROR, 'No json or data in json')
        abort(400)

    if request.json['event'] != 'created':
        logging.log(logging.ERROR, 'Event is not created')
        abort(400)

    # Check for Spark Key defined
    webhook_key = config.SPARK_WEBHOOK_SECRET

    # only validate if key is defined
    if webhook_key:
        # Validate webhook - https://developer.ciscospark.com/blog/blog-details-8123.html
        hashed = hmac.new(webhook_key, request.data, hashlib.sha1)
        expected_signature = hashed.hexdigest()
        signature = request.headers.get('X-Spark-Signature')
        if expected_signature != signature:
            logging.log(logging.ERROR, 'Invalid Spark Signature, expected %s but got %s' % (expected_signature, signature))
            abort(400)

    # Loop/echo prevention
    if request.json['data']['personEmail'] == config.SPARK_CUSTOMER_EMAIL:
        return "OK"

    # Connect to Spark API
    spark_api = ciscosparkapi.CiscoSparkAPI(access_token=config.SPARK_TOKEN)

    # Get the room info from room id that was passed from webhook
    room = spark_api.rooms.get(request.json['data']['roomId'])

    # Get the message
    message = spark_api.messages.get(request.json['data']['id'])

    # allow agents to privately exchange messages within context of the customer space
    # without sending a copy to the customer (agent whisper/notes)
    if message.mentionedPeople and message.mentionedPeople:
        return 'OK'

    # customer id is room name
    customer_id = room.title[-10:]

    # send SMS
    tropo.send_sms(customer_id, message.text)

    return 'OK'
