from .database import SessionLocal, Notification
import random

def send_email(content):
    print(f"[EMAIL]: {content}")
    if random.random() < 0.2:
        raise Exception("Email send failed (simulated)")
    return True

def send_sms(content):
    print(f"[SMS]: {content}")
    if random.random() < 0.2:
        raise Exception("SMS send failed (simulated)")
    return True

def process_notification(notification_obj):
    session = SessionLocal()
    notif = session.query(Notification).filter(Notification.id == notification_obj['id']).first()
    try:
        notif.status = "processing"
        session.commit()
        if notif.notification_type == "email":
            send_email(notif.content)
        elif notif.notification_type == "sms":
            send_sms(notif.content)
        notif.status = "sent"
        session.commit()
    except Exception as e:
        notif.status = "failed"
        session.commit()
        raise e
    finally:
        session.close()