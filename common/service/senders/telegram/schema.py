from common.schema import CoercedIntNullable, CustomBaseModel


class BaseTelegramMessageSchema(CustomBaseModel):
    chat_id: int


class SendTextMessageSchema(BaseTelegramMessageSchema):
    text: str
    reply_to: CoercedIntNullable
    # silent
    # background
    # reply_markup
