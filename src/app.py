"""
LabSync Phase 2 - Flask Backend Application
Smart Scheduling for Smarter Science

This Flask application provides a backend API for the LabSync resource booking system,
enhancing the Phase 1 client-side prototype with server-side persistence and multi-user support.
"""

import os
import json
import uuid
from datetime import datetime, date
from flask import Flask, request, jsonify, render_template, send_from_directory
from functools import wraps

app = Flask(__name__)

# Configuration
DATA_DIR = os.environ.get('DATA_DIR', './data')
os.makedirs(DATA_DIR, exist_ok=True)

RESOURCES_FILE = os.path.join(DATA_DIR, 'resources.json')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.json')

# Initialize default resources if not exists
DEFAULT_RESOURCES = [
    {"id": "microscope-a", "name": "Microscope A", "type": "equipment", "status": "available"},
    {"id": "microscope-b", "name": "Microscope B", "type": "equipment", "status": "available"},
    {"id": "cold-room-1", "name": "Cold Room 1", "type": "room", "status": "available"},
    {"id": "centrifuge", "name": "Centrifuge", "type": "equipment", "status": "available"},
    {"id": "pcr-machine", "name": "PCR Machine", "type": "equipment", "status": "available"}
]

def init_data_files():
    """Initialize data files with default values if they don't exist"""
    if not os.path.exists(RESOURCES_FILE):
        with open(RESOURCES_FILE, 'w') as f:
            json.dump(DEFAULT_RESOURCES, f, indent=2)
    
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, 'w') as f:
            json.dump([], f, indent=2)

def load_json_file(filepath, default=None):
    """Safely load JSON file with error handling"""
    if default is None:
        default = []
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        app.logger.error(f"Error loading {filepath}: {e}")
    
    return default

def save_json_file(filepath, data):
    """Safely save data to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError as e:
        app.logger.error(f"Error saving {filepath}: {e}")
        return False

def json_response(func):
    """Decorator to handle JSON responses and errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error in {func.__name__}: {e}")
            return jsonify({'error': str(e)}), 500
    return wrapper

def parse_time_to_minutes(time_str):
    """Convert time string (HH:MM) to minutes since midnight"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        return hours * 60 + minutes
    except ValueError:
        raise ValueError(f"Invalid time format: {time_str}")

def check_booking_conflict(resource_id, date_str, start_time, duration, exclude_id=None):
    """Check if a booking conflicts with existing bookings"""
    bookings = load_json_file(BOOKINGS_FILE)
    start_minutes = parse_time_to_minutes(start_time)
    end_minutes = start_minutes + int(duration)
    
    for booking in bookings:
        # Skip if this is the same booking (for updates)
        if exclude_id and booking.get('id') == exclude_id:
            continue
            
        # Check same resource and date
        if booking['resource_id'] == resource_id and booking['start_time'].split('T')[0] == date_str:
            booking_start = parse_time_to_minutes(booking['start_time'].split('T')[1][:5])
            booking_end = booking_start + booking['duration']
            
            # Check for overlap: max(start1, start2) < min(end1, end2)
            if max(start_minutes, booking_start) < min(end_minutes, booking_end):
                return True
    
    return False



# Routes

@app.route('/')
def dashboard():
    """Serve the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/resources')
@json_response
def get_resources():
    """Get list of all resources"""
    resources = load_json_file(RESOURCES_FILE, DEFAULT_RESOURCES)
    return jsonify(resources)

@app.route('/api/bookings')
@json_response
def get_bookings():
    """Get list of all bookings with optional filtering"""
    bookings = load_json_file(BOOKINGS_FILE)
    
    # Apply filters
    resource_filter = request.args.get('resource')
    date_filter = request.args.get('date')
    
    if resource_filter:
        bookings = [b for b in bookings if b.get('resource_id') == resource_filter or b.get('resource_name') == resource_filter]
    
    if date_filter:
        bookings = [b for b in bookings if b['start_time'].split('T')[0] == date_filter]
    
    # Sort by start time
    bookings.sort(key=lambda x: x['start_time'])
    
    return jsonify(bookings)

@app.route('/api/bookings', methods=['POST'])
@json_response
def create_booking():
    """Create a new booking"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user', 'resource_id', 'start_time', 'duration']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
    
    # Parse start time
    try:
        start_datetime = datetime.fromisoformat(data['start_time'].replace('Z', '+00:00'))
        date_str = start_datetime.date().isoformat()
        time_str = start_datetime.time().strftime('%H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid start_time format. Use ISO format (YYYY-MM-DDTHH:MM)'}), 400
    
    # Validate date is not in the past
    if start_datetime.date() < date.today():
        return jsonify({'error': 'Cannot book resources for past dates'}), 400
    
    # Check for conflicts
    if check_booking_conflict(data['resource_id'], date_str, time_str, data['duration']):
        return jsonify({'error': 'This time slot conflicts with an existing booking'}), 409
    
    # Get resource name
    resources = load_json_file(RESOURCES_FILE, DEFAULT_RESOURCES)
    resource_name = next((r['name'] for r in resources if r['id'] == data['resource_id']), data['resource_id'])
    
    # Create booking
    booking = {
        'id': str(uuid.uuid4()),
        'resource_id': data['resource_id'],
        'resource_name': resource_name,
        'user': data['user'].strip(),
        'start_time': data['start_time'],
        'duration': int(data['duration']),
        'timestamp': int(datetime.now().timestamp() * 1000)
    }
    
    # Save booking
    bookings = load_json_file(BOOKINGS_FILE)
    bookings.append(booking)
    
    if save_json_file(BOOKINGS_FILE, bookings):
        return jsonify(booking), 201
    else:
        return jsonify({'error': 'Failed to save booking'}), 500

@app.route('/api/bookings/<booking_id>', methods=['DELETE'])
@json_response
def delete_booking(booking_id):
    """Delete a booking"""
    bookings = load_json_file(BOOKINGS_FILE)
    
    # Find and remove booking
    original_count = len(bookings)
    bookings = [b for b in bookings if b['id'] != booking_id]
    
    if len(bookings) == original_count:
        return jsonify({'error': 'Booking not found'}), 404
    
    if save_json_file(BOOKINGS_FILE, bookings):
        return jsonify({'message': 'Booking deleted successfully'})
    else:
        return jsonify({'error': 'Failed to delete booking'}), 500

@app.route('/api/availability/<resource_id>')
@json_response
def get_availability(resource_id):
    """Get availability for a specific resource on a specific date"""
    date_param = request.args.get('date')
    if not date_param:
        return jsonify({'error': 'Date parameter is required'}), 400
    
    bookings = load_json_file(BOOKINGS_FILE)
    resource_bookings = [
        b for b in bookings 
        if b['resource_id'] == resource_id and b['start_time'].split('T')[0] == date_param
    ]
    
    # Sort by start time
    resource_bookings.sort(key=lambda x: x['start_time'])
    
    return jsonify({
        'resource_id': resource_id,
        'date': date_param,
        'bookings': resource_bookings,
        'available': len(resource_bookings) == 0
    })



@app.route('/api/stats')
@json_response
def get_stats():
    """Get booking statistics"""
    bookings = load_json_file(BOOKINGS_FILE)
    today = date.today().isoformat()
    
    # Calculate stats
    total_bookings = len(bookings)
    today_bookings = len([b for b in bookings if b['start_time'].split('T')[0] == today])
    
    # Calculate currently busy resources
    now = datetime.now()
    current_time_minutes = now.hour * 60 + now.minute
    busy_resources = set()
    
    for booking in bookings:
        if booking['start_time'].split('T')[0] == today:
            start_time_minutes = parse_time_to_minutes(booking['start_time'].split('T')[1][:5])
            end_time_minutes = start_time_minutes + booking['duration']
            
            if start_time_minutes <= current_time_minutes < end_time_minutes:
                busy_resources.add(booking['resource_id'])
    
    available_resources = len(DEFAULT_RESOURCES) - len(busy_resources)
    
    return jsonify({
        'total_bookings': total_bookings,
        'today_bookings': today_bookings,
        'available_resources': available_resources,
        'busy_resources': list(busy_resources)
    })

# Static file serving for development
@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize application
if __name__ == '__main__':
    init_data_files()
    
    # Development server configuration
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode)