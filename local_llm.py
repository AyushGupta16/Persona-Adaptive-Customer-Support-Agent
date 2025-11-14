# local_llm.py
from llama_cpp import Llama

# Path to your local GGUF model
MODEL_PATH = "models\llama-2-7b.Q2_K.gguf"

# Initialize once at import time (may take a bit on first load)
llm = Llama(
    model_path=MODEL_PATH,
    chat_format="llama-2",   # adjust based on model (e.g. "chatml")
    n_ctx=4096,              # context length, tune for your hardware
    n_threads=4              # adjust for your CPU
)

def chat(messages):
    """
    messages: list of dicts like OpenAI:
      [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    Returns the assistant content string.
    """
    result = llm.create_chat_completion(
        messages=messages,
        temperature=0.2
    )
    # llama-cpp-python returns an OpenAI-like structure
    return result["choices"][0]["message"]["content"]
