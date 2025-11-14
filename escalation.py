from typing import Dict
import datetime

ESCALATION_TRIGGERS = ["angry", "useless", "worst", "refund", "sue", "threat"]

def check_escalation(user_message: str, persona: str, docs: list) -> (bool, Dict):
    text = user_message.lower()
    escalate = False

    # Escalate if message contains any trigger words
    if any(trigger in text for trigger in ESCALATION_TRIGGERS):
        escalate = True

    # Escalate if persona is Frustrated User and no documents found
    if persona == "Frustrated User" and (not docs or len(docs) == 0):
        escalate = True

    handoff = None
    if escalate:
        handoff = {
            "time": datetime.datetime.utcnow().isoformat() + "Z",
            "persona": persona,
            "last_message": user_message,
            "kb_snippets": docs,
            "reason": "keyword_trigger_or_no_kb"
        }

    return escalate, handoff
