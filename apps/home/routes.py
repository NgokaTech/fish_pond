# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Dickson & Fredy.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import psycopg2
from psycopg2.extras import RealDictCursor

@blueprint.route('/index')
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/notifications')
@login_required
def notifications():
    # Database connection parameters
    DB_ENGINE = 'postgresql'
    DB_USERNAME = 'pest_db_user'
    DB_PASS = 'ic2ssRtlfJNayDEtbKkMhrvi6l4IyNJ8'
    DB_HOST = 'dpg-cqjkj2mehbks73cd0r30-a.oregon-postgres.render.com'
    DB_PORT = '5432'
    DB_NAME = 'pest_db'

    conn = None
    alerts = []

    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USERNAME,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )

        # Create a cursor to execute queries
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Fetch disease data from the database
        cursor.execute("SELECT disease, recommendation, image_path FROM disease_data ORDER BY detection_date DESC")
        disease_data = cursor.fetchall()

        # Create alerts list to pass to the template
        alerts = [{'disease': row['disease'], 'recommendation': row['recommendation'], 'image_path': row['image_path'], 'type': 'danger'} for row in disease_data]

    except Exception as e:
        print(f"Error fetching data: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

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
