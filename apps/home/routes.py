from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
import psycopg2
import base64
import logging
from jinja2 import TemplateNotFound

# Initialize Blueprint
blueprint = Blueprint('blueprint', __name__, template_folder='templates')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database connection parameters
DB_PARAMS = {
    'dbname': 'monitoring_db_j90f',
    'user': 'ngktch',
    'password': 'ykflTtg1uF6n0hUzuQoMexBeGRKXsqe4',
    'host': 'dpg-cq61miss1f4s73dqtut0-a.oregon-postgres.render.com',
    'port': '5432'
}

# Route for the home page (index)
@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

# Route for fetching notifications
@blueprint.route('/api/notifications', methods=['GET'])
@login_required
def get_notifications():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    # Query to fetch fish pond monitoring data
    cur.execute("SELECT object_count, ph_value, encode(image, 'base64') as image, timestamp FROM fish_pond_data ORDER BY timestamp DESC")
    rows = cur.fetchall()

    # Close the connection
    cur.close()
    conn.close()

    # Process the fish pond monitoring data into JSON format
    alerts = [
        {
            'object_count': row[0],
            'ph_value': row[1],
            'image': row[2],
            'timestamp': row[3].isoformat()
        }
        for row in rows
    ]

    # Log the fetched data
    logging.info(f"Fetched {len(alerts)} notifications")

    # Return the data as JSON
    return jsonify(alerts=alerts)

# Route for data insertion from Raspberry Pi
@blueprint.route('/api/upload', methods=['POST'])
def upload_data():
    object_count = request.form['object_count']
    ph_value = request.form['ph_value']
    image_data = request.files['image'].read()

    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO fish_pond_data (object_count, ph_value, image) VALUES (%s, %s, %s)",
        (object_count, ph_value, psycopg2.Binary(image_data))
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'status': 'success'}), 200

# Route for login page
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)  # Replace with your user authentication logic
        if user:
            login_user(user)
            return redirect(url_for('blueprint.index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Route for logout
@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('blueprint.index'))

# Catch-all route for custom templates
@blueprint.route('/<template>', methods=['GET'])
@login_required
def route_template(template):
    if not template.endswith('.html'):
        template += '.html'

    # Detect the current page
    segment = get_segment(request)

    # Serve the file (if exists) from app/templates/home/FILE.html
    return render_template("home/" + template, segment=segment)

# Helper - Extract current page name from request
def get_segment(request):
    segment = request.path.split('/')[-1]
    if segment == '':
        segment = 'index'
    return segment

# Replace this function with your actual user authentication logic
def authenticate_user(username, password):
    # Dummy user authentication logic
    # Replace with actual authentication logic
    if username == 'admin' and password == 'password':
        class User:
            is_authenticated = True
            is_active = True
            is_anonymous = False
            def get_id(self):
                return 1
        return User()
    return None
