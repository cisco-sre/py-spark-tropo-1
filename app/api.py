# This contains our api; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/
from flask import Blueprint, render_template, url_for, request, abort
from app import tropo
from app import spark

# Create blueprint object
api = Blueprint('api', __name__)

@api.route('/')
def index():
    """
    Our api index-page just shows a quick explanation from "templates/api.html"
    """
    return render_template('api.html')


@api.route('/tropo-webhook/', methods=['GET'])
def tropo_webhook_get():
    return render_template('tropo-webhook.html')


@api.route('/tropo-webhook/', methods=['POST'])
def tropo_webhook_post():
    # let flask build an external url based on SERVER_NAME. Must be done here so tropo.py doesn't require flask context
    webhook_url = url_for('.spark_webhook_post', _external=True)
    return tropo.webhook_process(request, webhook_url)


@api.route('/spark-webhook/', methods=['GET'])
def spark_webhook_get():
    return render_template('spark-webhook.html')


@api.route('/spark-webhook/', methods=['POST'])
def spark_webhook_post():
    """
    POST'd Data from Spark webhooks
    """
    return spark.webhook_process(request)


@api.route('/customer_room_message_post/', methods=['GET'])
def customer_room_post_message_get():
    return render_template('customer-room-post-message.html')


@api.route('/customer_room_message_post/', methods=['POST'])
def customer_room_post_message_post():
    """
    API endpoint to customer_room_post_message

Expects JSON data with customer_id and message
    """

    # make sure we have the data necessary to process the request
    if not request.json:
        abort(400)

    if not ('customer_id' in request.json and ('text' in request.json or 'markdown' in request.json)):
        abort(400)

    # let flask build an external url based on SERVER_NAME
    webhook_url = url_for('.spark_webhook_post', _external=True)

    # initialize dictionary with customer id
    args = {'customer_id': request.json['customer_id'], 'webhook_url':webhook_url}

    # loop over allowed API parameters to be passed to function and add if found in JSON
    allowed_parameters = ['text', 'markdown', 'files']
    for parameter in allowed_parameters:
        if parameter in request.json:
            args[parameter] = request.json[parameter]


    # pass customer id and upacked args to function
    message = spark.customer_room_message_send(request.json['customer_id'],**args)

    if not message:
       abort(500)

    return 'OK'
