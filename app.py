import flask
import threading
import time
import logging
from flask_cors import CORS
from questions import questions
from flask import jsonify
import random
import string
import Game from './game.py'

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str

class Team:
    def __init__(self):
        self.team_name = ""
        self.team_code = ""
        self.record = [] #

g = Game(questions)

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route('/get_status', methods=['GET'])
def getStatus():
    return g.getStatus()

@app.route('/get_questions', methods=['GET'])
def getQuestions():
    return jsonify(g.questions_list)

@app.route('/send_answer/<team_id>/<question_id>/<answer>', methods=['GET'])
def sendAnswer(team_id,question_id,answer):
    verification_queue.append([team_id,question_id,answer])

@app.route('/get_team_code/<team_name>', methods=['GET'])
def generateTeamCode(team_code):
    for t in g.rankings:
        if(t['teamName'] == team_name):
            return {'status' :-1,'message': 'team with this name already exists'}
    teamId = get_random_string(5)
    while(teamId in g.rankings):
        teamId = get_random_string(5)

    g.rankings[teamId] = {
        'teamId'   : teamId,
        'teamName' : team_name,
        'record'   : [0 for q in g.questions_list],
    }

@app.route('/start_game', methods=['GET'])
def startGame():
    g.start()
    return {'status':'game_started'}





if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
