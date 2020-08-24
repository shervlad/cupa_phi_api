import flask
import threading
import time
import logging
from flask_cors import CORS
from questions import questions
from flask import jsonify
import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))

    return result_str

class Team:
    def __init__(self):
        self.team_name = ""
        self.team_code = ""
        self.record = [] #

class Game:
    def __init__(self, questions_list):
        self.status = -1
        self.current_question = -1
        self.question_status = -1
        self.question_counter = -1
        self.reading_duration = -1
        self.thinking_duration = -1
        self.reading_timer = -1
        self.thinking_timer = -1
        self.waiting_timer = -1
        self.questions_list = questions_list

        self.rankings = {
            'team1id' : {
                    'teamId'   : 'asox023qe32nsdfsq', #some random string
                    'teamName' : 'The Bilzebobs',
                    'record'   : {'q1_id' : 0, 'q2_id' : 1, 'q3_id': 1, 'q4_id':0},
                    'answers'  : {
                                    'q1_id' : 'iarba verde',
                                    'q2_id' : 'gagarin',
                                    'q3_id' : 'frunzulita',
                                    'q4_id' : 'busuioc'
                                 },
                },

                'team2id' : {'q1_id' : 1, 'q2_id' : 1, 'q3_id': 0, 'q4_id':0},
                'team3id' : {'q1_id' : 0, 'q2_id' : 0, 'q3_id': 1, 'q4_id':1}
        }

    def getStatus(self):
        return {
            'status'                  : self.status,
            'question_counter'        : self.question_counter,
            'question_status'         : self.question_status,
            'reading_duration'        : self.reading_duration,
            'reading_timer'           : self.reading_timer,
            'thinking_duration'       : self.thinking_duration,
            'thinking_timer'          : self.thinking_timer,
            'waiting_timer'           : self.waiting_timer
        }

    def nextQuestion(self):
        self.question_counter += 1
        self.current_question_id = self.questions_list[self.question_counter]['question_id']


g = Game(questions)
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True



def loop(g):
    print("I'M IN THE LOOP!")
    while True:
        if(g.status == 'ongoing'):
            if(g.question_status == 'reading'):
                print("Question is being read")
                if(g.reading_timer < g.current_question['reading_duration']):
                    g.reading_timer = g.reading_timer + 1
                else:
                    g.question_status = 'thinking'
                    g.thinking_timer = 0

            elif(g.question_status == 'thinking'):
                print("people are thinking")
                if(g.thinking_timer < g.current_question['thinking_duration']):
                    g.thinking_timer = g.thinking_timer + 1
                else:
                    g.question_status = 'waiting_for_answers'
                    g.waiting_timer = 0

            elif(g.question_status == 'waiting_for_answers'):
                print("waiting for answers")
                if(g.waiting_timer < 10):
                    g.waiting_timer = g.waiting_timer + 1
                else:
                    g.question_couter = g.question_counter + 1
                    g.current_question = g.questions_list[g.question_counter]

                    if(g.question_counter>=len(g.questions_list)):
                        g.status = 'finished'
                    else:
                        g.question_status = 'reading'
                        g.reading_timer  = 0
                        g.thinking_timer = 0
                        g.waiting_timer  = 0
                        g.reading_duration = g.questions_list[g.question_counter]['reading_duration']
                        g.thinking_duration = g.questions_list[g.question_counter]['reading_duration']
            
        elif(g.status == 'finished'):
            print("GAME IS FINISHED")
            return

        print(g.getStatus())
        time.sleep(1)

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
    g.status = 'ongoing'
    g.question_status = 'reading'
    g.question_counter = 0
    g.current_question = g.questions_list[0]
    g.reading_timer = 0
    g.thinking_timer = 0

    x = threading.Thread(target=loop, args=(g,))
    x.start()
    return {'status':'game_started'}





if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
