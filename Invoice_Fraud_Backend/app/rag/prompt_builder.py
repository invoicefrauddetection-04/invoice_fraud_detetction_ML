from typing import List
from langchain_core.documents import Document

def format_retrieved_docs(docs: List[Document]) -> str:

    if not docs:
        return "No external knowledge retrieved."

    output = []

    for index, doc in enumerate(docs, start=1):

        source = doc.metadata.get("filename", "Unknown Source")

        category = doc.metadata.get("category", "Unknown")

        text = doc.page_content.strip()

        output.append(

            f"""
Document {index}

Source:
{source}

Category:
{category}

Content:
{text}
"""
        )

    return "\n\n".join(output) 

#==========================================================
# SHAP Explanation Formatter
#=========================================================

def format_shap(shap):

    if shap is None:

        return "SHAP explanation is not yet available."

    text = ""

    for feature in shap["top_features"]:

        text += f"""

Feature:
{feature['feature_name']}

Value:
{feature['feature_value']}

Contribution:
{feature['shap_value']}

"""

    return text


#=========================================================
# Main Prompt Builder
#=========================================================

def build_prompt(

    invoice_context,

    rag_docs,

    user_question

):
    document = invoice_context["document"]

    invoice = invoice_context["invoice"]

    prediction = invoice_context["prediction"]

    shap = invoice_context["shap"]

    prompt = f"""
        You are ProcureGuard AI.

        You are an AI assistant that explains invoice fraud predictions.

        Your job is to explain the prediction in clear, professional language.

        Never claim that the invoice is certainly fraudulent.

        Instead explain why the machine learning model considered it risky.

        Always use the retrieved procurement guidance whenever appropriate.

        --------------------------------------------------
        INVOICE
        --------------------------------------------------

        Image:
        {document["image_name"]}

        Supplier:
        {invoice["supplier_id"]}

        Invoice ID:
        {invoice["invoice_id"]}

        Invoice Date:
        {invoice["invoice_date"]}

        Country:
        {invoice["supplier_country"]}

        Amount:
        {invoice["total_amount"]}

        --------------------------------------------------
        MODEL PREDICTION
        --------------------------------------------------

        Prediction:
        {prediction["prediction"]}

        Fraud Probability:
        {prediction["fraud_probability"]}

        Model:
        {prediction["model_name"]}

        --------------------------------------------------
        SHAP EXPLANATION
        --------------------------------------------------

        {format_shap(shap)}

        --------------------------------------------------
        RETRIEVED KNOWLEDGE
        --------------------------------------------------

        {format_retrieved_docs(rag_docs)}

        --------------------------------------------------
        USER QUESTION
        --------------------------------------------------

        {user_question}

        --------------------------------------------------
        INSTRUCTIONS
        --------------------------------------------------

        Provide:

        1. Short explanation.

        2. Explain the most influential factors.

        3. Mention relevant procurement guidance.

        4. Suggest what an auditor should verify.

        Do not hallucinate.

        Do not invent facts.

        Do not state fraud as certain.

        Keep the answer under 300 words.
        """

    return prompt  

#==========================================================
# TESTING
#==========================================================

if __name__ == "__main__":
    from app.services.context_service import get_invoice_context
    from app.rag.retriever import retrieve_context

    context = get_invoice_context(59)
    docs = retrieve_context("Why was this invoice flagged?")

    prompt = build_prompt(
        invoice_context=context,
        rag_docs=docs,
        user_question="Why was this invoice flagged?"
    )

    print(prompt)