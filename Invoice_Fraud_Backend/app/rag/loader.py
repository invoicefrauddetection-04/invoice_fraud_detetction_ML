from pathlib import Path
import os

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)


# ---------------------------------------------------------
# Supported file extensions
# ---------------------------------------------------------

SUPPORTED_EXTENSIONS = {

    ".pdf",
    ".md",
    ".txt"

}


# ---------------------------------------------------------
# Load a single document
# ---------------------------------------------------------

def load_single_document(file_path: Path):

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        loader = PyPDFLoader(str(file_path))

        documents = loader.load()

    elif extension in [".md", ".txt"]:

        loader = TextLoader(

            str(file_path),

            encoding="utf-8"

        )

        documents = loader.load()

    else:

        return []

    category = file_path.parent.name

    for doc in documents:

        doc.metadata["filename"] = file_path.name

        doc.metadata["category"] = category

        doc.metadata["source"] = str(file_path)

    return documents


# ---------------------------------------------------------
# Load all documents recursively
# ---------------------------------------------------------
KNOWLEDGE_BASE = os.path.join(
    "app",
    "knowledge_base"
)

def load_documents(base_directory = KNOWLEDGE_BASE):

    base_path = Path(base_directory)

    all_documents = []

    for file_path in base_path.rglob("*"):

        if (

            file_path.is_file()

            and file_path.suffix.lower() in SUPPORTED_EXTENSIONS

        ):

            documents = load_single_document(file_path)

            all_documents.extend(documents)

    return all_documents


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

    print("Knowledge Base:", KNOWLEDGE_BASE)

    docs = load_documents(KNOWLEDGE_BASE)

    print("=" * 60)
    print("Total Documents Loaded :", len(docs))
    print("=" * 60)

    if docs:
        print(docs[0].metadata)