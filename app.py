import flask
import threading
import time
import logging
from flask_cors import CORS
from questions import questions
from flask import jsonify
import random
import string
from game import Game


class Team:
    def __init__(self):
        self.team_name = ""
        self.team_code = ""
        self.record = [] #

g = Game(questions)

app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
ADMIN_CODE = "i_am_the_admin"

@app.route('/get_status/<teamId>', methods=['GET'])
def getStatus(teamId):
    return jsonify(g.getStatus(teamId))

@app.route('/get_questions/<team_id>', methods=['GET'])
def getQuestions():
    return jsonify(g.questions_list)

@app.route('/send_answer/<team_id>/<member_name>/<question_id>/<answer>', methods=['GET'])
def sendAnswer(team_id,member_name,question_id,answer):
    verification_queue.append([team_id,member_name,question_id,answer])

@app.route('/register_team/<team_name>', methods=['GET'])
def registerTeam(team_name):
    return jsonify(g.registerTeam(team_name))

@app.route('/join/<team_id>', methods=['GET'])
def join(team_id):
    if(teamId == this.admin_code):
        return jsonify({'success':1,'data':g.getAdminStatus(team_id)})

    if(team_id not in g.history):
        return jsonify({
            'success' : -1,
            'message': 'team with this ID not registered'
        })
    else:
        return jsonify({'success':1,'data':g.getStatus(team_id)})

@app.route('/start_game/<admin_code>', methods=['GET'])
def startGame(admin_code):
    if(admin_code == ADMIN_CODE):
        g.start()
        return {'status': 1,
                'message':'game_started'}
    else:
        return {'status':-1,
                'message': 'you do not have authorization to perform this operation'}


@app.route('/get_verification_queue/<admin_code>', methods=['POST'])
def getVerificationQueue(admin_code):
    if(admin_code == ADMIN_CODE):
        data = g.getVerificationQueue()
        return {'status': 1,
                'data': data}
    else:
        return {'status':-1,
                'message': 'you do not have authorization to perform this operation'}

@app.route('/verify_answer/<admin_code>', methods=['POST'])
def verifyAnswer(admin_code):
    if(admin_code == ADMIN_CODE):
        submission = {
        'teamId'     : request.form['teamId'],
        'questionId' : request.form['questionId'],
        'check'      : request.form['check']

        }
        g.verify(submission)
        return {'status': 1,
                'message':'verified!'}
    else:
        return {'status':-1,
                'message': 'you do not have authorization to perform this operation'}


@app.route('/getRankings', methods=['GET'])
def getRankings():
    return g.getRankings()



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
