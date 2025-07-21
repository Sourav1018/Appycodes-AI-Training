from pydantic import BaseModel

class PromptRequest(BaseModel):
    message: str
