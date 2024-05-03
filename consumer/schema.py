from pydantic import BaseModel


class Message(BaseModel):
    type: str  # conversation_type key
    client_id: int

    text: str
