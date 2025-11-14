from local_llm import chat

TEMPLATES = {
    "Technical Expert": "Be concise and technical. Provide commands, diagnostics, and root-cause reasoning.",
    "Frustrated User": "Start with empathy, apologize briefly, provide a short step-by-step fix with minimal jargon.",
    "Business Executive": "High-level summary focusing on impact, timeline, and recommended next steps. Keep it short."
}

def generate_response(persona: str, docs: list, query: str) -> str:
    style = TEMPLATES.get(persona, "Be clear and helpful.")

    kb_context = "\n\n---\n\n".join(docs) if docs else "No relevant KB found."

    prompt = f"""
Persona: {persona}
Style instructions: {style}

User Query:
{query}

Relevant Knowledge Base:
{kb_context}

Task: Answer the user's query using the knowledge base and follow the style instructions.
Do NOT mention internal system details or that you are using personas.
"""

    messages = [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    return chat(messages)
