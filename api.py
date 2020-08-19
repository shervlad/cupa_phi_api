    # """
    # /api/start/gameid/teamid -> 


    # game loop

    #             current_question+=1
    #             timer = timelength(current_question)
    #             send audio to each team 
    #             wait till everybody gets it
    #             start timer : now everybody is playing the question
    #             wait till everybody read the question
    #             start 60sec timer
    #             receive answer or time out from all active users
    #             update score


    # on cline side:

    # update loop:
    #     ask for current quetion:
    #         if server_current_question != my_current_question:
    #             ask for question mp3
    #                 my_current_question = server_current_question
    #             play mp3
    #             start 60 sec timer
                

    # """
import flask
from flask import send_file, send_from_directory, safe_join, abort

import logging
import threading
import time


registered_teams = {
    'team1' : {
        'last_response': DateTime,
        'track_record': [1,0,1,0,0,-1,-1,-1,-1,-1,-1,-1]
    },
    'team2' : {
        'last_response': DateTime,
        'track_record': [1,0,1,0,0,-1,-1,-1,-1,-1,-1,-1]
    }
}

class Game:
    def __init__():
        current_question = -1
        status = 'not_started' #'sending','reading','waiting_for_answers'
        timer = -1
        registered_teams = []
        active_teams     = []

    def start():
        current_question = 0
        status='sending'

g = Game()
verification_queue = []

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/get_status/team_id', methods=['GET'])
def getStatus():
    return {'current_question':g.current_question,'status':g.status'}

def getTimer():
    return g.timer

@app.route('/get_question', methods=['GET'])
def getQuetion():
    return {'audio':None,'md':None}

@app.route('/submit_answer/qn/teamd_id/', methods=['GET'])
def submitAsnwer():
    #load mp3 from /questions/{q.current_question}/audio.mp3
    #if there is a file md.png in /questions/{q.current_questio}/, 
    #   load it
    return {'audio':None,'md':None}

def gameLoop():
    while True:
        for t in g.active_teams:
            if registered_teams[t]['last_response'] - time.now() > "10sec":
                #remove from active teams
                pass

        if(g.status == 'not_started'):
            g.status = 'sending'
            teams_who_received = []

        if(g.status == 'sending'):
            if len(teams_who_received) == len(active_teams):
                teams_who_received = []
                g.status = 'reading'

        if(g.status == 'reading'):
            if len(teams_who_finished_reading) == len(active_teams):
                teams_who_finished_reading = []
                g.status = 'waiting_for_answers'

        if(g.status == 'waiting_for_answer'):
            if len(teams_who_answered) == len(active_teams):
                teams_who_answered = []
                g.current_question += 1
                g.status = 'sending'

x = threading.Thread(target = gameLoop)
x.start()
app.run()
