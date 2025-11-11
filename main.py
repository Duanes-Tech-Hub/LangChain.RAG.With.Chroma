from library import genlib as genlib
from library import cdb as cdb
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import argparse

CHROMA_PATH = "chroma"
DATA_PATH = "data"
EMBEDDING_MODEL = "ollama"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('--query', type=str, default='What are the Monopoly rules?', help='Source directory containing PDFs')
    args = parser.parse_args()
    
    query_data = args.query


    #check if the chromadb does not exist and is not populated. Populate if everything is ok move on.
    if not cdb.check_chroma_db_populated(CHROMA_PATH):
        cdb.populate_chroma_db(CHROMA_PATH, DATA_PATH, EMBEDDING_MODEL)
        answer_text = query_llm(EMBEDDING_MODEL,query_data)
    else:
        answer_text = query_llm(EMBEDDING_MODEL,query_data)
    print(answer_text)

def query_llm(embedding: str, query_data: str)-> str:
    embedding_function = genlib.get_embedding(embedding)
    db = Chroma(
        client=cdb.CHROMA_CLIENT,
        collection_name="langchain",
        embedding_function=embedding_function
    )

    # Search the DB.
    results = db.similarity_search_with_score(query_data, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_data)
    # print(prompt)

    model = Ollama(model="mistral")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text

if __name__ == "__main__":
    main()