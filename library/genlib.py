from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
import lmstudio as lms

def get_ollama_embedding():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

def get_lmstudio_embedding():
    embeddings = lms.embedding_model("nomic-embed-text-v1.5")
    return embeddings

def get_huggingface_embedding(model_name="nomic-ai/nomic-embed-text-v1.5"):    
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings

def get_embedding(embedding: str):
    if embedding == "ollama":
        return get_ollama_embedding()
    elif embedding == "lmstudio":
        return get_lmstudio_embedding()
    else:
        return get_huggingface_embedding()