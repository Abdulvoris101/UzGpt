from gpt4all import GPT4All
from fastapi import APIRouter
from datetime import datetime
import time

modelRouter = APIRouter()

@modelRouter.on_event("startup")
async def on_startup():
    print("Running")

    global model
    model = GPT4All("ggml-model-gpt4all-falcon-q4_0.bin")
    print("Loaded model")

# model = None

class Completion:
    object_ = "completion"
    model = "falcon"


    def __init__(self, prompt, temperature, max_tokens, used, amount):
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.used = used
        self.amount = amount

    def generate(self):
        
        output = model.generate(
            self.prompt, 
            max_tokens=self.max_tokens, 
            temp=self.temperature
        )

        return output

    def complete(self):
        return {
            "object": self.object_,
            "created": datetime.now(),
            "model": self.model,
            "choices": [
                {
                    "index": 0,
                    "message": self.generate()
                }
            ],
            "used": self.used,
            "amount": self.amount,
            "currency": "sum"
        }


class ChatCompletion(Completion):
    object_ = "chat.completion"

    def __init__(self, messages, temperature, max_tokens, used, amount):
        self.messages = messages
        prompt = messages[-1]["content"]
        super().__init__(prompt, temperature, max_tokens, used, amount)

    
    def complete(self):
        model.current_chat_session = self.messages
        return {
            "object": self.object_,
            "created": datetime.now(),
            "model": self.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": self.generate(),
                    }
                }
            ],
            "used": self.used,
            "amount": self.amount,
            "currency": "sum"
        }
        