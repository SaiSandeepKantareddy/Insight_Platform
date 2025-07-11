# Agent-to-Agent Protocol (A2A)

from datetime import datetime

def create_a2a_message(sender, receiver, task, payload):
    return {
        "from": sender,
        "to": receiver,
        "task": task,
        "payload": payload,
        "timestamp": str(datetime.now())
    }
