from pydantic import BaseModel, Field


class History(BaseModel):
    """
    历史消息对话
    """
    role: str = Field(...)
    content: str = Field(...)