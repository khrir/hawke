from app.controllers.users_controller import UsersController
from app.controllers.events_controller import EventsController
from app.controllers.activities_controller import ActivitiesController
from flask import Blueprint, render_template, request, jsonify, session, url_for, redirect, g
from functools import wraps

users = UsersController()
events = EventsController()
activities = ActivitiesController()
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def before_request():
    if 'user' not in session:
        return redirect(url_for('user.login')) 
    g.user = session['user']
    g.user_id = g.user.get('id')

# Middleware para carregar o evento na sessão
@admin_bp.url_value_preprocessor
def load_event(endpoint, values):
    if values and 'id' in values:
        event_id = values['id']
        session.pop('current_event', None)

        event_data, _ = events.select(event_id)
        session['current_event'] = event_data['event']
        g.event = session['current_event']

def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.get('role_id') != 1:
            return redirect(url_for('admin.admin'))
        return f(*args, **kwargs)
    return decorated_function
    
@admin_bp.route('/users', methods=['GET'])
@is_admin
def users_view():    
    return render_template('users/list.html', users=users.list(), user=g.user)

@admin_bp.route('/events', methods=['GET'])
@is_admin
def events_view():
    return render_template('events/list.html', events=events.list(), user=g.user)

@admin_bp.route('/', methods=['GET'])
def admin():
    return render_template('admin/index.html', user=g.user)

# events administration routes 
@admin_bp.route('/my-events', methods=['GET'])
def view_organizer_events():
    return render_template('events/list.html', events=events.list_organizer_events(g.user.get('id')), user=g.user)

@admin_bp.route('/new-event', methods=['GET', 'POST'])
def event_create():
    if request.method == 'POST':
        response, status = events.create(request.form, g.user.get('id'))
        # print(response)
        # if status == 201:
        #     session['current_event'] = response['event']

        return jsonify(response), status

    return render_template('events/create.html', user=g.user)

@admin_bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
def event_edit(id):
    if request.method == 'POST':
        response, status = events.update(id, request.form)
        return jsonify(response), status
    
    return render_template('events/edit.html', user=g.user, event=g.event, isEventDashboard=True)

@admin_bp.route('/events/<int:id>/dashboard', methods=['GET'])
def event_dashboard(id):
    return render_template('events/dashboard.html', user=g.user, event=g.event, isEventDashboard=True)

# activities administration routes
@admin_bp.route('/events/<int:id>/activities', methods=['GET'])
def activity_view(id):
    res, _ = activities.list_by_event(id)
    return render_template('activities/index.html', event=g.event, activities=res['activities'], user=g.user, isEventDashboard=True)

@admin_bp.route('/events/<int:id>/new-activity', methods=['GET', 'POST'])
def activity_create(id):
    if request.method == 'POST':
        response, status = activities.create(request.form)
        return jsonify(response), status
    
    return render_template('activities/create.html', user=g.user, event=g.event, isEventDashboard=True)

@admin_bp.route('/activities/<int:id>/edit', methods=['POST'])
def activity_edit(id):
    response, status = activities.update(id, request.form)
    return jsonify(response), status