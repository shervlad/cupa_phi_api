import random
import string
import threading

class Game:
    def __init__(self, questions_list):
        self.status = 'not_started'
        self.current_question = -1
        self.question_status = -1
        self.question_counter = -1
        self.reading_duration = -1
        self.thinking_duration = -1
        self.reading_timer = -1
        self.thinking_timer = -1
        self.waiting_timer = -1
        self.questions_list = questions_list

        self.game_thread = None

        self.history = {
            'team1id' : {
                    'team_id'   : 'asox023qe32nsdfsq', #some random string
                    'team_name' : 'The Bilzebobs',
                    'record'   : {'q1_id' : 0, 'q2_id' : 1, 'q3_id': 1, 'q4_id':0},
                    'answers'  : {
                        'q1_id' : { 'raspuns': 'iarba verde', 'team_member': 'vasilika'},
                        'q2_id' : { 'raspuns': 'gagarin',     'team_member': 'vasilika'},
                        'q3_id' : { 'raspuns': 'tsoi jiv',    'team_member': 'vasilika'},
                        'q4_id' : { 'raspuns': 'ligma',       'team_member': 'vasilika'},
                    },
                    'scor' : 0
                }
        }

        self.rankings = {
            'team1' : [0,0,1,0,1,0,0,1,0,1,0,-1,-1,-1,-1,-1],
            'team2' : [0,1,9,1,1,0,0,1,0,1,0,-1,-1,-1,-1,-1],
            'team3' : [0,0,1,1,1,1,0,1,0,1,0,-1,-1,-1,-1,-1],
            'team4' : [0,0,1,0,1,0,1,1,0,1,1,-1,-1,-1,-1,-1],
            'team5' : [0,0,1,0,1,0,0,1,0,1,0,-1,-1,-1,-1,-1]
        }

        self.verification_queue = []

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(length))

        return result_str

    def getStatus(self, team_id):
        return {
            'status'                  : self.status,
            'question_counter'        : self.question_counter,
            'question_status'         : self.question_status,
            'reading_duration'        : self.reading_duration,
            'reading_timer'           : self.reading_timer,
            'thinking_duration'       : self.thinking_duration,
            'thinking_timer'          : self.thinking_timer,
            'waiting_timer'           : self.waiting_timer,
            'team_history'            : self.history[team_id]
        }

    def revise(self,teamId, questionId, check):
        self.history[teamId]['record'][qiestionId] = check

    def updateRankings(self):
        questionset_structure = [{'q1'},{'q2a','q2b'},{'q3'},{'q4'},{'q5'}]
        tmp_rankings = {}
        for teamId in self.history:
            tmp_rankings[teamId] = [-1 for i in range(len(self.questions_list))]
        for qno, qstruct in enumerate(questionset_structure):
            for teamId in self.rankings:
                teamAnsweredCorrectly = True
                teamHasntAnsweredYet  = False
                for questionid in qstruct:
                    if(self.rankings[teamId]['record'][questionId] == -1):
                        teamHasntAnsweredYet = True
                    if(self.rankings[teamId]['record'][questionId] == 0):
                        teamAnsweredCorrectly = False
                if(teamHasntAnsweredYet):
                    rankings[teamId][qno] = -1
                else:
                    rankings[teamId][qno] = int(teamAnsweredCorrectly)


    def getRankings(self):
        return self.rankings

    def start(self):
        self.status            = 'ongoing'
        self.question_counter  = 0
        self.question_status   = 'reading'
        self.current_question  = self.questions_list[self.question_counter]
        self.reading_duration  = self.current_question['reading_duration']
        self.thinking_duration = self.current_question['thinking_duration']

        self.reading_timer     = 0
        self.thinking_timer    = 0
        self.waiting_timer     = 0

        self.game_thread = threading.Thread(target=self.loop, args=(self))
        self.game_thread.start()

    def verify(self,submission):
        teamId     = submission['teamId']
        questionId = submission['questionId']
        check      = submission['check']
        self.history[teamId]['record'][questionId] = check


    def getNextUnverified(self):
        return self.verification_queue[-1]

    def submitAnswer(self,teamId,teamMember,questionId, answer):
        self.rankings[teamId]['answers'][questionId]['answer'] = answer
        self.rankings[teamId]['answers'][questionId]['team_member'] = team_member
        self.verification_queue.append({'teamId':teamId,'questionId':questionId,'answer':answer})

    def nextQuestion(self):
        self.question_counter  = self.question_counter + 1

        if(self.question_counter>=len(self.questions_list)):
            self.status = 'finished'

        self.current_question  = self.questions_list[self.question_counter]


        self.question_status   = 'reading'
        self.reading_timer     = 0
        self.thinking_timer    = 0
        self.waiting_timer     = 0
        self.reading_duration  = self.questions_list[self.question_counter]['reading_duration']
        self.thinking_duration = self.questions_list[self.question_counter]['reading_duration']

    def loop(self):
        print("I'M IN THE LOOP!")
        while True:
            if(self.question_status == 'reading'):
                print("Question is being read")
                if(self.reading_timer < self.current_question['reading_duration']):
                    self.reading_timer = self.reading_timer + 1
                else:
                    self.question_status = 'thinking'
                    self.thinking_timer = 0

            elif(self.question_status == 'thinking'):
                print("people are thinking")
                if(self.thinking_timer < self.current_question['thinking_duration']):
                    self.thinking_timer = self.thinking_timer + 1
                else:
                    self.question_status = 'waiting_for_answers'
                    self.waiting_timer = 0

            elif(self.question_status == 'waiting_for_answers'):
                print("waiting for answers")
                if(self.waiting_timer < 10):
                    self.waiting_timer = self.waiting_timer + 1
                else:
                    self.nextQuestion()

            elif(self.status == 'finished'):
                print("GAME IS FINISHED")
                return

            print(self.getStatus())
            time.sleep(1)

    def registerTeam(self,team_name):
        for team_id, team_object in self.history.items():
            if(team_object['team_name'] == team_name):
                return {'status' :-1,'message': 'team with this name already exists'}

        team_id = self.get_random_string(5)
        while(team_id in self.history):
            team_id = get_random_string(5)

        self.history[team_id] = {
            'team_id'   : team_id,
            'team_name' : team_name,
            'record'    : [0 for q in self.questions_list],
            'answers'   : {},
            'score'     : 0
        }

        self.rankings[team_id] = [0 for q in self.questions_list]

        return {'success':1, 'team_id':team_id}

