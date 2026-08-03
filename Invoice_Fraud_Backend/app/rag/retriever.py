from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_DB = BASE_DIR / "vector_db" / "faiss_index"


embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vector_store = FAISS.load_local(
    folder_path=str(VECTOR_DB),
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)


retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k":5
    }
)

def retrieve_context(question: str):

    docs = retriever.invoke(question)

    return docs 

#=========================================================
# TESTING
#=========================================================

if __name__ == "__main__":

    query = "Why are duplicate invoices considered fraudulent?"

    docs = retrieve_context(query)

    print("=" * 60)
    print("Retrieved Chunks :", len(docs))
    print("=" * 60)

    for i, doc in enumerate(docs, start=1):

        print(f"\nResult {i}")

        print("-" * 40)

        print(doc.page_content[:700])

        print("\nMetadata:")

        print(doc.metadata)