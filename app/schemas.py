from pydantic import BaseModel, Field

class NotificationCreate(BaseModel):
    user_id: int
    notification_type: str = Field(..., pattern="^(email|sms|inapp)$")
    content: str

class NotificationRead(BaseModel):
    id: int
    user_id: int
    notification_type: str
    content: str
    status: str

    class Config:
        from_attributes = True