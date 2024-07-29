from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
import requests
import json

# Define the API endpoint and key
API_ENDPOINT = "https://monitoring-system-va17.onrender.com/api/disease_data"
API_KEY = "rnd_cfn28WFvfPJhRZwtj5WrStCCP8D8"

@blueprint.route('/index')  
@login_required
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/notifications')
@login_required
def notifications():
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Fetch disease data from the API
        response = requests.get(API_ENDPOINT, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        disease_data = response.json()
        
        # Create alerts list to pass to the template
        alerts = [
            {
                'disease': entry['disease'],
                'recommendation': entry['recommendation'],
                'image_path': entry['image_path'],
                'type': 'danger'
            }
            for entry in disease_data
        ]
    
    except requests.RequestException as e:
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
