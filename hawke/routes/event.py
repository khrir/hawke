from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from app.controllers.events_controller import EventsController
from app.controllers.activities_controller import ActivitiesController
from app.controllers.event_users_controller import EventUsersController
import os, dotenv

dotenv.load_dotenv()

events = EventsController()
activities = ActivitiesController()
event_users = EventUsersController()
event_bp = Blueprint('event', __name__)

# <string:slug>
@event_bp.route('/<string:slug>', methods=['GET'])
def view(slug):
    mp_public_key = os.getenv('MP_PUBLIC_KEY')

    event = events.select_by_slug(slug) # its a tuple
    event = event[0]['event']
    address = event['address']
    link = (address['local'] + ' - ' + address['zip_code'] + ', ' + address['city'] + ', ' + address['state'] + ', Brasil')
    act_list, _ = activities.list_by_event(event['id'])

    return render_template('events/index.html', event=event, address=address, link=link, activities=act_list['activities'], public_key=mp_public_key)

@event_bp.route('/subscribe', methods=['POST'])
def subscribe():
    response, status = event_users.create(request.form)
    return jsonify(response), status

@event_bp.route('/event/<int:event_id>/get_subscriptions', methods=['GET'])
def get_subscriptions(event_id):
    response = event_users.get_subscriptions(event_id)
    return jsonify(response), 200