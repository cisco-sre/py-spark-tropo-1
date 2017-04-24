# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

from flask import Blueprint, render_template, flash, redirect, url_for, request

from .forms import ContactForm

from app import spark

frontend = Blueprint('frontend', __name__)

# Simple Homepage
@frontend.route('/')
def index():
    return render_template('index.html')

# Simple contact form
@frontend.route('/contact/', methods=('GET', 'POST'))
def contact():
    form = ContactForm()

    if request.method == 'POST' and form.validate():
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        flash('We got your message and will get back to you soon!')

        #form.message.data
        #form.phone.data

        # send to customers room
        webhook_url = url_for('api.spark_webhook_post', _external=True)
        spark.customer_room_message_send(form.phone.data, text=form.message.data, webhook_url=webhook_url)
        form.data.clear()

        # In a real application, you may wish to avoid this tedious redirect.
        return redirect(url_for('.index'))

    return render_template('contact.html', form=form)
