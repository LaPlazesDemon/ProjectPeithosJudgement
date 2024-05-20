from flask import Flask, jsonify, app, request
import analyze
import json

with open('config.json') as f:
    config = json.load(f)


app = Flask(__name__)
app.config['HOST'] = config['host']
app.config['PORT'] = config['port']

@app.route('/analyze', methods=['GET'])
def start_analysis():
    
    userid = request.args.get('userid')

    if (not userid):
        return jsonify({"error": "userid is a required parameter"}, 400)
    
    return analyze.analyze_user(userid)
    
app.run(
    host = config['host'],
    port = config['port'],
    debug = True
)