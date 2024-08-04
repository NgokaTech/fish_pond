from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
import psycopg2
import base64
import logging

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
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Query to fetch rail inspection data
        cur.execute("SELECT defect_type, description, encode(image, 'base64') as image, geo_location, detection_date FROM rail_inspection_data ORDER BY detection_date DESC")
        rows = cur.fetchall()

        # Close the connection
        cur.close()
        conn.close()

        # Process the rail inspection data into JSON format
        alerts = [
            {
                'defect_type': row[0],
                'description': row[1],
                'image': row[2],
                'geo_location': row[3],
                'detection_date': row[4].isoformat()
            }
            for row in rows
        ]

        # Log the fetched data
        logging.info(f"Fetched {len(alerts)} notifications")

        # Return the data as JSON
        return jsonify(alerts=alerts)

    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify(alerts=[]), 500  # Return an empty list and a 500 status code in case of error

# Route for data insertion from Raspberry Pi
@blueprint.route('/api/upload', methods=['POST'])
def upload_data():
    try:
        defect_type = request.form['defect_type']
        description = request.form['description']
        geo_location = request.form['geo_location']
        image_data = request.files['image'].read()

        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO rail_inspection_data (defect_type, description, image, geo_location) VALUES (%s, %s, %s, %s)",
            (defect_type, description, psycopg2.Binary(image_data), geo_location)
        )
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        logging.error(f"Error uploading data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Route for login page
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user.authenticate(username, password)  # Replace with your user authentication logic
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
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except Exception as e:
        logging.error(f"Error loading template: {e}")
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except Exception as e:
        logging.error(f"Error extracting segment: {e}")
        return None
