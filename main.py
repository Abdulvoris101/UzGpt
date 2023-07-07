from gpt4all import GPT4All

model = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")

print("Loaded model!")


def answer(messages):
    output = model.generate(messages[-1]["content"], max_tokens=200)

    model.current_chat_session = messages
    
    return output

