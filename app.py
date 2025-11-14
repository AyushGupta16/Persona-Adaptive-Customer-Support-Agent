from fastapi import FastAPI
from pydantic import BaseModel
from retriever import load_kb, retrieve_docs
from persona_classifier import detect_persona
from response_generator import generate_response
from escalation import check_escalation

app = FastAPI(title="Persona-Adaptive Support Agent")

# Load knowledge base into a ChromaDB collection once at startup
collection = load_kb()

class QueryIn(BaseModel):
    message: str

class AgentOut(BaseModel):
    persona: str
    response: str
    escalated: bool = False
    handoff: dict | None = None

@app.post("/support", response_model=AgentOut)
async def support(query: QueryIn):
    user_message = query.message

    # Detect persona locally
    persona_info = detect_persona(user_message)
    persona = persona_info.get("persona", "Business Executive")

    # Retrieve relevant KB docs
    docs, metadatas = retrieve_docs(user_message, collection)

    # Determine escalation need
    escalate, handoff = check_escalation(user_message, persona, docs)

    if escalate:
        return AgentOut(persona=persona, response="Escalating to human agent...", escalated=True, handoff=handoff)

    # Generate persona-adaptive response locally
    final_response = generate_response(persona, docs, user_message)

    return AgentOut(persona=persona, response=final_response, escalated=False, handoff=None)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
