from transformers import T5Tokenizer, T5ForConditionalGeneration

# print("Here1")
class AskLLM:
    def __init__(self) -> None:
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

    def ask_llm(self, prompt):
        print("Prompt to LLM is :", prompt)
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("Response from LLM is : ", response)
        return response

