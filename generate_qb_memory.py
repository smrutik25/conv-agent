import json
import random
from read_json_config import read_json
"""
{
"Q1":{"question":"",
"options":["","","",""],
"answered_before":True/False,
"correct_answer":"",

"given_answer":""
"is_correct":True/False,
"context":"quiz"
}
}

"""
def generate_qb_topic(topic="BODMAS"):
    #fetch from RAG
    question_bank = open("sample_questions.json").read()
    question_bank = json.loads(question_bank)
    no_of_questions = read_json("TOTAL_QUESTIONS")
    
    previous_questions = []
    prev_incorrect_questions = []
    new_questions = []

    for question in question_bank:
        if "is_correct" in question and question["topic"] == topic:
            previous_questions.append(question)
            if not question["is_correct"]:
                prev_incorrect_questions.append(question)
        else:
            new_questions.append(question)

    if len(new_questions) >= (no_of_questions - len(previous_questions)):
        ask_questions = random.sample(new_questions, no_of_questions - len(prev_incorrect_questions))
    else:
        ask_questions = new_questions
    ask_questions.extend(prev_incorrect_questions)

    return ask_questions

def qb_other_topics(topic="BODMAS"):
    question_bank = open("sample_questions.json").read()
    question_bank = json.loads(question_bank)
    
    prev_incorrect_questions = []
    for question in question_bank:
        if "is_correct" in question and not question["is_correct"] and question["topic"]!=topic:
            prev_incorrect_questions.append(question)

    return prev_incorrect_questions
    
