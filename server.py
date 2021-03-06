import os
from flask import Flask, request, redirect, g, render_template, jsonify
import twilio.twiml
import logging



DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)


numbers = set()
projects = [
{"name": "Cara for President", "votes":0},
{"name": "Olivia for President", "votes":0},
{"name": "E for President", "votes":0},
{"name": "Ari for President", "votes":0},
{"name": "Emilio for President", "votes":0},
{"name": "Ryan for President", "votes":0},
]

@app.route('/')
def index():
    return render_template('index.html', projects=projects)

@app.route('/list')
def list():
    return jsonify(projects=projects)

@app.route('/vote', methods=['POST'])
def vote():
    from_number = request.form['From']
    # number exists
    resp = twilio.twiml.Response()
    if from_number in numbers:
        resp.sms("Thanks, but you already voted!")
    else:
        body = request.form['Body'].strip().upper()
        letters = "ABCDEFGHIJKLMNOP"
        ident = letters.find(body)
        if len(body) != 1 or ident == -1 or ident >= len(projects):
            resp.sms('That is an invalid vote, please try again!')
        else:
            projects[ident]['votes'] += 1
            numbers.add(from_number)
            resp.sms('Thank you for your vote!')
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
