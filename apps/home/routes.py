from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import psycopg2

# Define your database connection details
DB_CONFIG = {
    'dbname': 'pest_db',
    'user': 'pest_db_user',
    'password': 'ic2ssRtlfJNayDEtbKkMhrvi6l4IyNJ8',
    'host': 'dpg-cqjkj2mehbks73cd0r30-a.oregon-postgres.render.com',
    'port': '5432'
}

@blueprint.route('/index')  
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/notifications')
@login_required
def notifications():
    try:
        # Connect to the database
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Fetch disease data from the database
        cur.execute("SELECT disease, recommendation, image_path FROM disease_data ORDER BY detection_date DESC")
        rows = cur.fetchall()
        
        # Close connection
        cur.close()
        conn.close()
        
        # Create alerts list to pass to the template
        alerts = [
            {
                'disease': row[0],
                'recommendation': row[1],
                'image_path': row[2],
                'type': 'danger'
            }
            for row in rows
        ]
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        alerts = []

    return render_template('home/notifications.html', alerts=alerts)

@blueprint.route('/<template>')
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

    except:
        return render_template('home/page-500.html'), 500

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
