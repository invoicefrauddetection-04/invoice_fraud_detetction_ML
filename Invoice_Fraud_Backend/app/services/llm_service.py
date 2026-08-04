import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from app.services.context_service import get_invoice_context

from app.rag.retriever import retrieve_context

from app.rag.prompt_builder import build_prompt


load_dotenv()


MODEL_NAME = os.getenv("GEMINI_MODEL")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


llm = ChatGoogleGenerativeAI(

    model=MODEL_NAME,

    google_api_key=GOOGLE_API_KEY,

    temperature=0.2

)


def generate_ai_explanation(

    document_id: int,

    question: str

):

    invoice_context = get_invoice_context(document_id)

    if invoice_context["status"] != "success":

        return invoice_context

    rag_docs = retrieve_context(question)

    sources = []

    seen = set()

    for doc in rag_docs:

        key = doc.metadata["filename"]

        if key not in seen:

            seen.add(key)

            sources.append({

                "filename": doc.metadata["filename"],

                "category": doc.metadata.get("category"),

                "page": doc.metadata.get("page")

            })

    prompt = build_prompt(

        invoice_context=invoice_context,

        rag_docs=rag_docs,

        user_question=question

    )

    response = llm.invoke(prompt)

    answer = response.content
    if isinstance(answer, list):
        answer = answer[0]["text"]

    return {

        "status": "success",

        "document_id": document_id,

        "sources": sources,

        "answer": answer

    } 


#==========================================================
# TESTING
#==========================================================
if __name__ == "__main__":

    result = generate_ai_explanation(

        document_id=59,

        question="Why was this invoice flagged?"

    )

    print(result["answer"])

    from pprint import pprint

    pprint(result)