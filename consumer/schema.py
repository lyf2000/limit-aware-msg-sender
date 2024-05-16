from common.schema import CustomBaseModel


class ConsumerMessage(CustomBaseModel):
    # type: str  # conversation_type key
    client_id: int

    text: str
