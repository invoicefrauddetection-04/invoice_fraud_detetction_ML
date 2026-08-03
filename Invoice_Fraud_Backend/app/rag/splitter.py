from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.loader import load_documents


# --------------------------------------------------------
# Split Documents
# --------------------------------------------------------

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=800,

        chunk_overlap=200,

        separators=[

            "\n\n",

            "\n",

            ". ",

            " ",

            ""

        ]

    )

    chunks = splitter.split_documents(documents)

    return chunks


# --------------------------------------------------------
# Testing
# --------------------------------------------------------

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent
    
    KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

    docs = load_documents(KNOWLEDGE_BASE)

    chunks = split_documents(docs)

    print("=" * 60)

    print("Original Documents :", len(docs))

    print("Chunks Generated :", len(chunks))

    print("=" * 60)

    print("\nSample Chunk:\n")

    print(chunks[0].page_content)

    print("\nMetadata:\n")

    print(chunks[0].metadata)