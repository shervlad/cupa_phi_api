import flask
import threading
import time
import logging
from flask_cors import CORS

class Game:
    def __init__(self):
        self.status = 'not_started'
        self.reading_timer = -1
        self.thinking_timer = -1
        self.waiting_timer = -1
        self.current_question = -1
        self.question_status = 'None'
        self.questions = [
            {
                'audio'       :'https://www.dropbox.com/s/t6w3pr344zbio67/q1.mp3?raw=1',
                'audio_length': 32,
                'md'          :'https://i.kym-cdn.com/entries/icons/facebook/000/012/431/gig.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/y134n6y37vp4mwi/q2.mp3?raw=1',
                'audio_length': 40,
                'md'          :'https://wasabi-files.lbstatic.nu/files/looks/medium/2017/07/04/5212737_IMG_20170704_202541_607.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/psgiztbch5r2i30/q3.mp3?raw=1',
                'audio_length': 16,
                'md'          :'https://i.pinimg.com/originals/76/72/1a/76721a0f8fe44970cbadedad2c891ac5.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/t6w3pr344zbio67/q1.mp3?raw=1',
                'audio_length': 32,
                'md'          :'https://i.kym-cdn.com/entries/icons/facebook/000/012/431/gig.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/y134n6y37vp4mwi/q2.mp3?raw=1',
                'audio_length': 40,
                'md'          :'https://wasabi-files.lbstatic.nu/files/looks/medium/2017/07/04/5212737_IMG_20170704_202541_607.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/psgiztbch5r2i30/q3.mp3?raw=1',
                'audio_length': 16,
                'md'          :'https://i.pinimg.com/originals/76/72/1a/76721a0f8fe44970cbadedad2c891ac5.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/t6w3pr344zbio67/q1.mp3?raw=1',
                'audio_length': 32,
                'md'          :'https://i.kym-cdn.com/entries/icons/facebook/000/012/431/gig.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/y134n6y37vp4mwi/q2.mp3?raw=1',
                'audio_length': 40,
                'md'          :'https://wasabi-files.lbstatic.nu/files/looks/medium/2017/07/04/5212737_IMG_20170704_202541_607.jpg'
            },
            {
                'audio'       :'https://www.dropbox.com/s/psgiztbch5r2i30/q3.mp3?raw=1',
                'audio_length': 16,
                'md'          :'https://i.pinimg.com/originals/76/72/1a/76721a0f8fe44970cbadedad2c891ac5.jpg'
            }
        ]

    def getStatus(self):
        return {
            'status'          :self.status,
            'reading_timer'   :self.reading_timer,
            'thinking_timer'  :self.thinking_timer,
            'waiting_timer'   :self.waiting_timer,
            'current_question':self.current_question,
            'question_status' :self.question_status
        }
    def startOver(self):
        self.status = 'not_started'
        self.reading_timer = -1
        self.thinking_timer = -1
        self.waiting_timer = -1
        self.current_question = -1
        self.question_status = 'None'


g = Game()
app = flask.Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


def loop(g):
    print("I'M IN THE LOOP!")
    while True:
        if(g.status=='not_started'):
            g.status = 'ongoing'
            g.current_question = 0
            g.question_status = 'reading'
            g.reading_timer = g.questions[g.current_question]['audio_length']

        elif(g.status == 'ongoing'):
            if(g.question_status == 'reading'):
                if(g.reading_timer > 0):
                    g.reading_timer = g.reading_timer - 1
                else:
                    g.question_status = 'thinking'
                    g.thinking_timer = 5
            elif(g.question_status == 'thinking'):
                if(g.thinking_timer > 0):
                    g.thinking_timer = g.thinking_timer - 1
                else:
                    g.question_status = 'waiting_for_answers'
                    g.waiting_timer = 5
            elif(g.question_status == 'waiting_for_answers'):
                if(g.waiting_timer > 0):
                    g.waiting_timer = g.waiting_timer - 1
                else:
                    g.current_question = g.current_question + 1
                    if(g.current_question>=len(g.questions)):
                        g.status = 'finished'
                    else:
                        g.question_status = 'reading'
                        g.reading_timer = g.questions[g.current_question]['audio_length']
        elif(g.status=='finished'):
            g.startOver()
        time.sleep(1)

@app.route('/get_status', methods=['GET'])
def getStatus():
    return g.getStatus()

@app.route('/get_question', methods=['GET'])
def getQuestion():
    return g.questions[g.current_question]

x = threading.Thread(target=loop, args=(g,))
x.start()

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)