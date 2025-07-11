from datetime import datetime
import uuid

def create_acp_message(sender, receiver, task, payload, intent="DeliverFinalInsight"):
    return {
        "protocol": "ACP",
        "message_id": str(uuid.uuid4()),
        "sender": sender,
        "receiver": receiver,
        "task": task,
        "intent": intent,
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload
    }
