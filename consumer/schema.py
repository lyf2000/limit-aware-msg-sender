from pydantic import BaseModel


class ConsumerMessage(BaseModel):
    type: str  # conversation_type key
    client_id: int

    text: str
