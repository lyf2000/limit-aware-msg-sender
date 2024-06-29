from common.schema import CoercedInt, CoercedIntNullable, CustomBaseModel


class BaseTelegramMessageSchema(CustomBaseModel):
    chat_id: CoercedInt


class SendTextMessageSchema(BaseTelegramMessageSchema):
    text: str
    reply_to: CoercedIntNullable
    # silent
    # background
    # reply_markup
