# Runs local LLM via Ollama
from langchain_community.llms import Ollama

def load_llm(model_name="mistral"):
    return Ollama(model=model_name, temperature=0.7)