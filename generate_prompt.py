import json
from read_json_config import fill_template
from query_llm import AskLLM

class PromptGenerator:
    def __init__(self, llm):
        self.llm = llm
        with open("config.json") as jsonfile:
            self.config = json.load(jsonfile)["PROMPTS"]

    #TO-DO : Add ask LLM here only instead of returning prompt
            
    # def ask_intent(self, raw_text, length = "1"):
    #     self.prompt = "Give the intent of the following in " + length + " words: " + raw_text
    #     return self.prompt
    
    # def compare_intents(self, intent_1, intent_2):
    #     self.prompt = "Are the following intents the same? " + intent_1 + " and " + intent_2
    #     return self.prompt

    def prompt_generator_dialogue(self, user_dialogue, prompt_type):
        prompt = fill_template(["DIALOGUE"], [user_dialogue], self.config[prompt_type])
        # ask llm 
        llm_response = self.llm.ask_llm(prompt)
        return llm_response.lower().strip()

    def prompt_generator(self, prompt):
        # ask llm 
        llm_response = self.llm.ask_llm(prompt)
        return llm_response.lower().strip()
    
if __name__ == "__main__":
    prompts = PromptGenerator(AskLLM())
    response = prompts.prompt_generator_dialogue("Hi I am good","COHERENT_DIALOGUE")
    print(response)
    response = prompts.prompt_generator_dialogue("Hi I am Smruti","NAME")
    print(response)
    response = prompts.prompt_generator_dialogue("Yeah I'm good","YES_NO")
    print(response)
    response = prompts.prompt_generator_dialogue("Let's go with geometry","TOPIC")
    print(response)
    response = prompts.prompt_generator("The user got a mathematics question right and is showing happy emotion. Answer yes/no whether user needs a break?")
    print(response)
    response = prompts.prompt_generator("The user got a mathematics question right and is showing neutral emotion. Please give one suitable facial expression out of the following: Smile, Frown, Sadness, Surprise.")
    print(response)
    response = prompts.prompt_generator_dialogue("yes let's go","YES_NO")
    print(response)
    