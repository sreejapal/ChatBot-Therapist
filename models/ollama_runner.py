# Runs local LLM via Ollama
from langchain_ollama import OllamaLLM
import time

def load_llm(model_name="mistral"):
    try:
        # Try to create the Ollama instance
        llm = OllamaLLM(model=model_name, temperature=0.7)
        
        # Test the connection with a simple prompt
        test_response = llm.invoke("Hello")
        print(f"[DEBUG] Ollama connection successful with model: {model_name}")
        return llm
    except Exception as e:
        print(f"[ERROR] Failed to connect to Ollama: {e}")
        print("[INFO] Make sure Ollama is running with: ollama serve")
        print("[INFO] And the model is available with: ollama list")
        raise e