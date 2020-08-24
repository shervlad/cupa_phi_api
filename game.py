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

        self.rankings = {
            'team1id' : {
                    'teamId'   : 'asox023qe32nsdfsq', #some random string
                    'teamName' : 'The Bilzebobs',
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

        x = threading.Thread(target=self.loop, args=(this))
        x.start()
    
    def verify(self,submission)
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

