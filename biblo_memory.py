from furhat_connection import FurhatConnection
from generate_prompt import PromptGenerator
from db_conn import DBConn
from read_json_config import read_json, fill_template
from generate_qb_memory import generate_qb_topic


class Biblo:
    def __init__(self) -> None:
        self.furhat_conn = FurhatConnection()
        self.prompt_generator = PromptGenerator()
        self.user_id = 0
        self.sql_conn = DBConn()  
        self.user_id = 0
        self.user_name = ""
        #llm connection

    def introduce(self):
        try:
            user, new_user = self.sql_conn.fetch_current_user()
            self.user_id = user[0]
            if new_user:
                intro_template = read_json("INTRODUCTION_NEW_USER")
                self.furhat_conn.furhat_speak(intro_template["1"])
                self.furhat_conn.furhat_speak(intro_template["2"])
                user_dialogue = self.furhat_conn.furhat_listen()
                user_name = self.prompt_generator(user_dialogue, "NAME")
                self.sql_conn.update_name(self.user_id,user_name)
                self.user_name = user_name
                bot_dialogue = fill_template(["NAME"], [user_name], intro_template["3"])
            
            elif not new_user:
                intro_template = read_json("INTRODUCTION_RETURNING_USER")
                self.furhat_conn.furhat_speak(intro_template["1"])
                self.user_name = user[1]  # get name from response
                bot_dialogue = fill_template(["NAME"], [self.user_name], intro_template["2"])
            
            self.furhat_conn.furhat_speak(bot_dialogue)
            user_dialogue = self.furhat_conn.furhat_listen()
            study_flag = self.prompt_generator(user_dialogue, "YES_NO")
            if study_flag == 'yes':
                return True, user_dialogue
            else:
                return False, user_dialogue
        
        except Exception as e:
            raise Exception(e)


    def choose_topic(self, user_dialogue):
        try:
            topic_templates = read_json("TOPICS")
            self.furhat_conn.furhat_speak(topic_templates["1"])
            user_dialogue = self.furhat_conn.furhat_listen()
            topic_chosen = self.prompt_generator(user_dialogue, "TOPIC")
            if topic_chosen not in read_json("LIST_OF_TOPICS"):
                self.furhat_conn.furhat_speak(topic_templates["2"])
                user_dialogue = self.furhat_conn.furhat_listen()
                topic_flag = self.prompt_generator(user_dialogue, "YES_NO")
                if topic_flag == 'yes':
                    topic_chosen = "general"
                else:
                    topic_chosen = self.prompt_generator(user_dialogue, "TOPIC")
                    if topic_chosen not in read_json("LIST_OF_TOPICS"):
                        topic_chosen = "general"
                    
            bot_dialogue = fill_template(["TOPIC"], [topic_chosen], topic_templates["2"])
            self.furhat_conn.furhat_speak(bot_dialogue)
            return topic_chosen
            
        except Exception as e:
            raise Exception(e)
        
    def quiz(self, topic_chosen):
        context = "quiz"
        try:
            qb = generate_qb_topic(topic_chosen)
            for question in qb:
                question_ui = {key: question[key] for key in ["question","options","correct"]}
                #TODO: render question
                
                self.furhat_conn.furhat_speak(question["question"])
                for option in question["question"]:
                    self.furhat_conn.furhat_speak(option)

                

                

                #fetch answer from UI 
                choice = "a"
                if choice == question["correct"]:
                    is_correct = True
                    
                    #correct answer given
                else:
                    #incorrect answer given
                    is_correct = False
                #give result (correct or wrong)
                #detect emotion
                pass

        except Exception as e:
            raise Exception(e)
    
    def general_talk(self):
        try:
            pass
        except Exception as e:
            raise Exception(e)
        
    def talk(self):
        to_study, user_dialogue = self.introduce()
        if not to_study:
            self.general_talk(user_dialogue)
        self.choose_topic(user_dialogue)

            



