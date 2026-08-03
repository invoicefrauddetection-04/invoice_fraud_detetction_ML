import os

from langchain_community.vectorstores import FAISS

from app.rag.loader import load_documents
from app.rag.splitter import split_documents
from app.rag.embeddings import get_embedding_model


# ----------------------------------------------------
# Build FAISS Index
# ----------------------------------------------------

def build_vector_store():

    print("=" * 60)
    print("Loading Documents...")
    print("=" * 60)

    documents = load_documents()

    print(f"Loaded : {len(documents)} documents")

    print("=" * 60)
    print("Splitting Documents...")
    print("=" * 60)

    chunks = split_documents(documents)

    print(f"Chunks : {len(chunks)}")

    print("=" * 60)
    print("Loading Embedding Model...")
    print("=" * 60)

    embedding_model = get_embedding_model()

    print("=" * 60)
    print("Generating Embeddings...")
    print("=" * 60)

    vector_store = FAISS.from_documents(

        documents=chunks,

        embedding=embedding_model

    )

    save_path = os.path.join(

        "app",

        "vector_db",

        "faiss_index"

    )

    os.makedirs(save_path, exist_ok=True)

    vector_store.save_local(save_path)

    print("=" * 60)
    print("FAISS Index Saved Successfully")
    print(save_path)
    print("=" * 60)

    return vector_store


# ----------------------------------------------------
# Load Existing Index
# ----------------------------------------------------

def load_vector_store():

    embedding_model = get_embedding_model()

    save_path = os.path.join(

        "app",

        "vector_db",

        "faiss_index"

    )

    return FAISS.load_local(

        save_path,

        embedding_model,

        allow_dangerous_deserialization=True

    )


# ----------------------------------------------------
# Test
# ----------------------------------------------------

if __name__ == "__main__":

    build_vector_store()