from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.schemas import NotificationCreate, NotificationRead
from app.database import SessionLocal, Notification, create_db
from app.queue import publish_notification

app = FastAPI(
    title="Notification Service API (MySQL)",
    description="Send notifications to users using MySQL & RabbitMQ.",
    version="1.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notifications", response_model=NotificationRead)
def send_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    notif = Notification(
        user_id=notification.user_id,
        notification_type=notification.notification_type,
        content=notification.content,
        status="pending"
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    publish_notification({"id": notif.id})
    return notif

@app.get("/users/{id}/notifications", response_model=list[NotificationRead])
def get_user_notifications(id: int, db: Session = Depends(get_db)):
    notifs = db.query(Notification).filter(Notification.user_id==id).order_by(Notification.created_at.desc()).all()
    return notifs