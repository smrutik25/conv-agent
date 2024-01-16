from furhat_connection import FurhatConnection
from generate_prompt import PromptGenerator
from query_llm import AskLLM
from db_conn import DBConn
from read_json_config import read_json, fill_template
from generate_qb import generate_qb_topic
import random
import time
import math


class Biblo:
    def __init__(self) -> None:
        self.llm = AskLLM()
        self.furhat_conn = FurhatConnection(self.llm)
        self.prompter = PromptGenerator(self.llm)
        self.user_id = 0
        self.sql_conn = DBConn()  
        self.user_id = 1
        self.user_name = ""

    def introduce(self):
        try:
            user, new_user = self.sql_conn.fetch_current_user()
            self.user_id = user[0]
            if new_user:
                intro_template = read_json("INTRODUCTION_NEW_USER")
                self.furhat_conn.furhat_speak(intro_template["1"])
                self.furhat_conn.furhat_speak(intro_template["2"])
                user_dialogue = self.furhat_conn.furhat_listen()
                user_name = self.prompter.prompt_generator_dialogue(user_dialogue, "NAME")
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
            study_flag = self.prompter.prompt_generator_dialogue(user_dialogue, "YES_NO")
            print("Study flag: ",study_flag)
            
            if study_flag == 'yes':
                return True, user_dialogue
            else:
                return False, user_dialogue
        
        except Exception as e:
            raise Exception(e)


    def choose_topic(self):
        try:
            topic_templates = read_json("TOPICS")
            self.furhat_conn.furhat_speak(topic_templates["1"])
            user_dialogue = self.furhat_conn.furhat_listen()
            topic_chosen = self.prompter.prompt_generator_dialogue(user_dialogue, "TOPIC")
            print("Topic chosen 1:", topic_chosen)
            if topic_chosen not in read_json("LIST_OF_TOPICS"):
                self.furhat_conn.furhat_speak(topic_templates["2"])
                user_dialogue = self.furhat_conn.furhat_listen()
                topic_flag = self.prompter.prompt_generator_dialogue(user_dialogue, "YES_NO")
                if topic_flag == 'yes':
                    print("Topic chosen 2:", topic_chosen)
                    topic_chosen = "general"
                else:
                    topic_chosen = self.prompter.prompt_generator_dialogue(user_dialogue, "TOPIC")
                    print("Topic chosen 3:", topic_chosen)
                    if topic_chosen not in read_json("LIST_OF_TOPICS"):
                        topic_chosen = "general"
                    
            bot_dialogue = fill_template(["TOPIC"], [topic_chosen], topic_templates["3"])
            self.furhat_conn.furhat_speak(bot_dialogue)
            return topic_chosen
            
        except Exception as e:
            raise Exception(e)
        
    def quiz(self, topic_chosen):
        context = "quiz"
        correct_questions, incorrect_questions = 0,0
        total_questions = read_json("TOTAL_QUESTIONS")
        emotion_prompts = read_json("PROMPTS")
        try:
            qb = generate_qb_topic(topic_chosen)
            quiz_dialogue = read_json("QUIZ_DIALOGUE")
            started = False
            for question in qb:
                if started:
                    self.furhat_conn.furhat_speak(random.choice(quiz_dialogue["NEXT_QUESTION"]))
                started = True
                question_ui = {key: question[key] for key in ["question","options","correct"]}
                
                #TODO: render question
                
                self.furhat_conn.furhat_speak(question["question"])
                self.furhat_conn.furhat_speak("The options are: ")
                for option in question["options"]:
                    self.furhat_conn.furhat_speak(option)

                # TODO: while answer not set from UI
                # wait for answer for 45s
                
                time.sleep(10)
                self.furhat_conn.furhat_speak(random.choice(quiz_dialogue["ASK_FOR_HINT"]))
                user_dialogue = self.furhat_conn.furhat_listen()
                hint_wanted = self.prompter.prompt_generator_dialogue(user_dialogue, "YES_NO")
                if hint_wanted == 'yes':
                    self.furhat_conn.furhat_speak(question["hint"])
                    
                # TODO: while answer not set from UI
                # wait for answer for 45s
                time.sleep(5)
                
                # TODO: fetch answer from UI 
                choice = "a"
                if choice == question["correct"]:
                    is_correct = True
                    correct_questions += 1
                    # render on UI, correct answer
                    if correct_questions < math.floor(total_questions/2):
                        self.furhat_conn.furhat_speak(random.choice(quiz_dialogue["CORRECT_ANSWER"]))
                    else:
                        self.furhat_conn.furhat_speak(random.choice(quiz_dialogue["MANY_CORRECT_ANSWERS"]))

                    user_answer = "correct" if is_correct else "incorrect"
                    llm_prompt = fill_template(["RIGHT/WRONG","EMOTION"], [user_answer, emotion], emotion_prompts["EMOTION_EXPRESSION"])
                    llm_resp = self.llm.ask_llm(llm_prompt)
                    self.furhat_conn.furhat_gesture(llm_resp)
                    self.furhat_conn.furhat_speak("Would you like to hear the working?")
                    user_dialogue = self.furhat_conn.furhat_listen()
                    explanation_wanted = self.prompter.prompt_generator_dialogue(user_dialogue, "YES_NO")
                    if explanation_wanted == 'yes':
                        self.furhat_conn.furhat_speak(question["explanation"])

                else:
                    is_correct = False
                    incorrect_questions += 1
                    # render on UI, incorrect answer
                    if correct_questions < math.floor(total_questions/2):
                        self.furhat_conn.furhat_speak(random.choice(quiz_dialogue["INCORRECT_ANSWER"]))
                    else:
                        self.furhat_conn.furhat_speak(random.choice(quiz_dialogue["MANY_INCORRECT_ANSWERS"]))
                    
                    user_answer = "correct" if is_correct else "incorrect"
                    llm_prompt = fill_template(["RIGHT/WRONG","EMOTION"], [user_answer, emotion], emotion_prompts["EMOTION_EXPRESSION"])
                    llm_resp = self.llm.ask_llm(llm_prompt)
                    self.furhat_conn.furhat_gesture(llm_resp)
                    self.furhat_conn.furhat_speak(question["explanation"])

                #detect emotion
                emotion = self.sql_conn.fetch_emotion(self.user_id)
                if emotion == "" or emotion == None:
                    emotion = "Neutral"
                
                llm_prompt = fill_template(["RIGHT/WRONG","EMOTION"], [user_answer, emotion], emotion_prompts["EMOTION_DIALOGUE"])
                llm_resp = self.llm.ask_llm(llm_prompt)
                if llm_resp == 'yes':
                    #switch to general talk
                    self.general_talk()
            
            return correct_questions, incorrect_questions                    
# if session terminates midway, have the finally block setup properly
# in biblo memory, add another block to ask to revise incorrect questions from other topics if any

        except Exception as e:
            raise Exception(e)
    
    def session_end(self, correct_questions,incorrect_questions): 
        if correct_questions > incorrect_questions:
            performance = str(correct_questions-incorrect_questions)
        else:
            performance = "1"
        performance_specific = read_json("PERFORMANCE_SPECIFIC_DIALOGUE")[performance]
        bot_dialogue = fill_template(["CORRECT","INCORRECT","PERFORMANCE_SPECIFIC"], [str(correct_questions),str(incorrect_questions),performance_specific], read_json("SESSION_END_DIALOGUE"))
        self.furhat_conn.furhat_speak(bot_dialogue)
        return
    
    
    def general_talk(self):
        try:
            bot_dialogue = random.choice(read_json("GENERAL_TALK"))
            self.furhat_conn.furhat_speak(bot_dialogue)
            keep_talking = True
            dialog_length = 0
            while keep_talking:
                user_dialogue = self.furhat_conn.furhat_listen()
                dialog_length += 1
                # if user says I don't want to do this, stop
                bot_dialogue = self.prompter.prompt_generator_dialogue(user_dialogue)
                self.furhat_conn.furhat_speak(bot_dialogue)
                if not dialog_length%2:
                    bot_dialogue = read_json("GENERAL_TO_QUIZ_DIALOGUE")
                    self.furhat_conn.furhat_speak(bot_dialogue)
                    user_dialogue = self.furhat_conn.furhat_listen()
                    to_study = self.prompter.prompt_generator_dialogue(user_dialogue, "YES_NO")
                    if to_study == 'yes':
                        return
                    else:
                       bot_dialogue = self.prompter.prompt_generator_dialogue(user_dialogue)
                       self.furhat_conn.furhat_speak(bot_dialogue) 


                
        except Exception as e:
            raise Exception(e)
        
    def talk(self):
        try:
            # to_study, user_dialogue = self.introduce()
            # # flag, dialog = self.introduce()
            # topic = self.choose_topic()
            # c, w = self.quiz(topic)
            # # c, w = 3,0
            # self.session_end(c,w)
            self.general_talk()

        
        #TODO: following code
        # if not to_study:
        #     self.general_talk(user_dialogue)
        # self.choose_topic(user_dialogue)
        except Exception as e:
            print(e)
            raise(e)
        finally:
            print("Done")
            #TODO: put in all session end things like db conn and all

            
if __name__ == "__main__":
    Biblo().talk()


