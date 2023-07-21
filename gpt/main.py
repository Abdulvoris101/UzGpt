from gpt4all import GPT4All
from fastapi import APIRouter
from datetime import datetime
import time
import copy
from sse_starlette.sse import EventSourceResponse
import json
from fastapi.concurrency import run_in_threadpool

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


    def __init__(self, prompt, temperature, stream, max_tokens, used, amount):
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.used = used
        self.stream = stream
        self.amount = amount

    def generate(self):         
        template = "You are helpfull assistant and also you to be friendly. "   
        output = model.generate(
            template + self.prompt, 
            max_tokens=self.max_tokens,
            temp=self.temperature
        )
        
        return output


    async def completion_to_chunks(self, chat=[]):
        model.current_chat_session = chat
        template = "You are helpfull assistant. "   

        for output in model.generate(
            template + self.prompt,
            max_tokens=self.max_tokens,
            temp=self.temperature,
            streaming=True,
            
        ):
            yield {
                "object": self.object_,
                "created": str(datetime.now()),
                "model": self.model,
                "choices": [
                    {
                        "index": 0,
                        "content": output
                    }
                ],
                "used": self.used,
                "amount": self.amount,
                "currency": "sum"
            }
            

    async def complete(self):
        if self.stream:
            return self.completion_to_chunks()
        else:
            return {
                "object": self.object_,
                "created": str(datetime.now()),
                "model": self.model,
                "choices": [
                    {
                        "index": 0,
                        "content": self.generate() 
                    }
                ],
                "used": self.used,
                "amount": self.amount,
                "currency": "sum"
            }


class ChatCompletion(Completion):
    object_ = "chat.completion"

    def __init__(self, messages, temperature, stream, max_tokens, used, amount):
        self.messages = messages

        prompt = messages[-1]["content"]

        super().__init__(prompt, temperature, stream, max_tokens, used, amount)

    
    async def complete(self):
        model.current_chat_session = self.messages
        
        if self.stream:
            return self.completion_to_chunks(self.messages)

        return {
            "object": self.object_,
            "created": datetime.now(),
            "model": self.model,
            "choices": [
                {
                    "index": 0,
                    "content": self.generate()
                }
            ],
            "used": self.used,
            "amount": self.amount,
            "currency": "sum"
        }