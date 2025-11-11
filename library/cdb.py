import os
import shutil
from . import genlib as genlib
from chromadb import PersistentClient, Settings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma

# Shared client to avoid multiple instances with different settings
CHROMA_CLIENT = PersistentClient(
    path="chroma",  # This should match CHROMA_PATH from main.py
    settings=Settings(allow_reset=True, anonymized_telemetry=False)
)

def check_chroma_db_populated(db_path: str) -> bool:
    """
    Checks if a ChromaDB instance exists at the specified path and is populated.

    A database is considered "populated" if:
    1. The directory structure exists.
    2. A Chroma PersistentClient can be initialized from the path.
    3. The client lists at least one collection.
    4. At least one collection contains one or more documents.

    Args:
        db_path: The file system path where the Chroma database is expected to be stored.

    Returns:
        True if the database is populated, False otherwise.
    """
    print(f"-> Checking ChromaDB path: '{db_path}'")

    # 1. Check for basic directory existence
    if not os.path.exists(db_path):
        print(f"   [FAIL] Path does not exist: '{db_path}'")
        return False
    
    # 2. Try to initialize the client and check for collections
    try:

        # List all existing collections, from the shared client
        collections = CHROMA_CLIENT.list_collections()
        
        if not collections:
            print("   [FAIL] Database exists, but no collections found.")
            return False

        print(f"   [INFO] Found {len(collections)} collection(s). Checking document count...")

        # 3. Check if any collection has documents
        for collection in collections:
            count = collection.count()
            print(f"   [INFO] Collection '{collection.name}' has {count} document(s).")
            if count > 0:
                print("   [SUCCESS] Database exists and is populated with documents.")
                return True
        
        # If the loop finishes, all collections were empty
        print("   [FAIL] Database exists, but all found collections are empty.")
        return False

    except Exception as e:
        # This catch handles errors during client initialization (e.g., if the directory 
        # exists but doesn't have the correct internal Chroma files).
        print(f"   [ERROR] Failed to initialize Chroma client or access data at '{db_path}'.")
        print(f"   Error Details: {e}")
        print("   This might indicate an invalid ChromaDB structure, even if the directory exists.")
        return False

def reset_chroma_db(db_path: str) -> None:
    """
    Deletes the ChromaDB directory at the specified path, effectively resetting the database.

    Args:
        db_path: The file system path where the Chroma database is stored.
    """
    if os.path.exists(db_path):
        print(f"-> Resetting ChromaDB at path: '{db_path}'")
        try:
            shutil.rmtree(db_path)
            print("   [SUCCESS] ChromaDB reset successfully.")
        except Exception as e:
            print(f"   [ERROR] Failed to delete ChromaDB directory: {e}")
    else:
        print(f"   [INFO] No ChromaDB found at '{db_path}' to reset.")

def populate_chroma_db(db_path: str, db_data: str, embedding : str) -> None:
    documents = load_documents(db_data)
    chunks = split_documents(documents)
    add_to_chroma(db_path, embedding, chunks)
    
def load_documents(db_data: str) -> list[Document]:
    document_loader = PyPDFDirectoryLoader(db_data)
    return document_loader.load()

def split_documents(documents: list[Document]) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(db_path: str, embedding : str, chunks: list[Document]):
    # Use the shared client instead of persist_directory
    db = Chroma(
        client=CHROMA_CLIENT,
        collection_name="langchain",
        embedding_function=genlib.get_embedding(embedding)
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks