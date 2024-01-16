from transformers import T5Tokenizer, T5ForConditionalGeneration

# print("Here1")
# tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xxl")
# print("Here2")
# model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xxl")


tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

input_text = "translate English to German: How old are you?"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))

input_text = "What is the intent of the sentence in two words: I do not want to study"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))

input_text = "What is the intent of the sentence in one word: The answer is d 500"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))

input_text = "What is the intent of the sentence in one word: I do not understand"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))

input_text = "What is the intent of the sentence in one word: Bye"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))

input_text = "What is the name of the person saying the following: Hi, I am Smruti"
input_ids = tokenizer(input_text, return_tensors="pt").input_ids
outputs = model.generate(input_ids)
print(tokenizer.decode(outputs[0]))
print(tokenizer.decode(outputs[0],skip_special_tokens=True))
