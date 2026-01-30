from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime  # <--- Added this

app = Flask(__name__)

DB_FILE = 'scores.json'


def load_scores():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_score(name, db_level, pitch):
    scores = load_scores()

    # We now save the TIMESTAMP
    scores.append({
        'name': name,
        'score': float(db_level),
        'pitch': int(pitch),
        'date': datetime.now().isoformat()  # <--- Saves "2026-01-30T10:00:00"
    })

    # Keep last 2000 scores (plenty for a new site)
    if len(scores) > 2000:
        scores = scores[-2000:]

    with open(DB_FILE, 'w') as f:
        json.dump(scores, f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/record_score', methods=['POST'])
def record_score():
    data = request.json
    save_score(
        data.get('name', 'Anonymous'),
        data.get('score', 0),
        data.get('pitch', 0)
    )
    return jsonify({'status': 'success'})


@app.route('/api/get_leaderboard')
def get_leaderboard():
    return jsonify(load_scores())


if __name__ == '__main__':
    app.run(debug=True, port=5000)