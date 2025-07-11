from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)

EVENTS_FILE = 'events.json'
PARTICIPANTS_FILE = 'participants.json'

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    events = load_data(EVENTS_FILE)
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        events = load_data(EVENTS_FILE)
        event_id = request.form['event_id']
        events[event_id] = {
            'name': request.form['name'],
            'date': request.form['date'],
            'venue': request.form['venue']
        }
        save_data(EVENTS_FILE, events)
        return redirect('/')
    return render_template('add_event.html')

@app.route('/register/<event_id>', methods=['GET', 'POST'])
def register(event_id):
    if request.method == 'POST':
        participants = load_data(PARTICIPANTS_FILE)
        if event_id not in participants:
            participants[event_id] = []
        participants[event_id].append({
            'name': request.form['name'],
            'email': request.form['email'],
        })
        save_data(PARTICIPANTS_FILE, participants)
        return redirect('/')
    return render_template('register.html', event_id=event_id)

@app.route('/participants/<event_id>')
def participants(event_id):
    participants = load_data(PARTICIPANTS_FILE)
    event_participants = participants.get(event_id, [])
    return render_template('participants.html', participants=event_participants, event_id=event_id)

if __name__ == '__main__':
    app.run(debug=True)
