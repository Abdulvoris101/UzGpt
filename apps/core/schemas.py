from pydantic import BaseModel, Field
import typing


class ChatBody(BaseModel):
    role: typing.Literal["system", "user", "assistant"] = Field(
        default="user", description="The role of the message."
    )
    content: str


class ChatCompletionCreate(BaseModel):
    messages: typing.List[ChatBody]
    max_tokens: int = Field(
        default=16, ge=1, le=2048, description="The maximum number of tokens to generate."
    )
    temperature: float = Field(
        default=0.8,
        ge=0.0,
        le=2.0,
        description="Adjust the randomness of the generated text.\n\n"
        + "Temperature is a hyperparameter that controls the randomness of the generated text. It affects the probability distribution of the model's output tokens. A higher temperature (e.g., 1.5) makes the output more random and creative, while a lower temperature (e.g., 0.5) makes the output more focused, deterministic, and conservative. The default value is 0.8, which provides a balance between randomness and determinism. At the extreme, a temperature of 0 will always pick the most likely next token, leading to identical outputs in each run.",
    )
    
    class Config:
        schema_extra = {
            "example": {
                "messages": [
                    ChatBody(
                        role="user", content="What is the capital of France?"
                    ),
                ],
                "max_tokens": 16
            }
        }


class CompletionCreate(BaseModel):
    prompt: str
    max_tokens: int = Field(
        default=16, ge=1, le=2048, description="The maximum number of tokens to generate."
    )
    temperature: float = Field(
        default=0.8,
        ge=0.0,
        le=2.0,
        description="Adjust the randomness of the generated text.\n\n"
        + "Temperature is a hyperparameter that controls the randomness of the generated text. It affects the probability distribution of the model's output tokens. A higher temperature (e.g., 1.5) makes the output more random and creative, while a lower temperature (e.g., 0.5) makes the output more focused, deterministic, and conservative. The default value is 0.8, which provides a balance between randomness and determinism. At the extreme, a temperature of 0 will always pick the most likely next token, leading to identical outputs in each run.",
    )
    
    class Config:
        schema_extra = {
            "example": {
                "prompt": "What's capital of France?",
                "max_tokens": 16
            }
        }
