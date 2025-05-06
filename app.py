from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS   # ← add this
import json

app = Flask(__name__, static_folder='static')
CORS(app) 

# load or init fake DB
try:
    with open('db.json') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {
      'userPrefs': [],
      'listings': [
        {"id":1, "title":"Cozy 1-BR","rent":900,"neighborhood":"Porta Romana","url":"…"},
        {"id":2, "title":"Loft near Duomo","rent":1200,"neighborhood":"Duomo","url":"…"}
      ]
    }

@app.route('/')
def landing():
    return send_from_directory('static', 'index.html')

@app.route('/userPrefs', methods=['POST'])
def save_prefs():
    prefs = request.json
    data['userPrefs'].append(prefs)
    with open('db.json','w') as f:
        json.dump(data, f, indent=2)
    return jsonify(success=True), 200

@app.route('/listings')
def listings():
    max_rent = request.args.get('rent_lte', type=int)
    if max_rent:
        return jsonify([l for l in data['listings'] if l['rent'] <= max_rent])
    return jsonify(data['listings'])

if __name__=='__main__':
    app.run(port=3001, debug=True)