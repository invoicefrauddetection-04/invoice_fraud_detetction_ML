// ===================================
// ProcureGuard AI
// AI Investigator
// ===================================

const documentId =
    localStorage.getItem("currentDocumentId");

const noInvoiceState =
    document.getElementById("noInvoiceState");

const investigatorChat =
    document.getElementById("investigatorChat");

const documentIdDisplay =
    document.getElementById("documentIdDisplay");

const investigatorInput =
    document.getElementById("investigatorInput");

const investigatorSendBtn =
    document.getElementById("investigatorSendBtn");

const chatMessages =
    document.getElementById("chatMessages");


console.log(
    "AI Investigator Document ID:",
    documentId
);


// -----------------------------------
// Check whether invoice was analyzed
// -----------------------------------

if (!documentId) {

    noInvoiceState.style.display = "block";
    investigatorChat.style.display = "none";

}
else {

    noInvoiceState.style.display = "none";
    investigatorChat.style.display = "flex";

    documentIdDisplay.textContent =
        `#${documentId}`;

}

// -----------------------------------
// Send question to LLM
// -----------------------------------

function addUserMessage(message) {

    const messageElement = document.createElement("div");

    messageElement.className =
        "message user-message";

    messageElement.innerHTML = `
        <div class="message-content"></div>
    `;

    messageElement
        .querySelector(".message-content")
        .textContent = message;

    chatMessages.appendChild(messageElement);

    messageElement.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}

function addAssistantMessage(message, sources = []) {

    const messageElement = document.createElement("div");

    messageElement.className =
        "message assistant-message";

    messageElement.innerHTML = `
        <div class="message-icon">
            <i class="fa-solid fa-robot"></i>
        </div>

        <div class="message-content">
            <div class="assistant-answer"></div>
        </div>
    `;

    const content =
        messageElement.querySelector(".assistant-answer");

    const parsedMarkdown =
        marked.parse(message);

    content.innerHTML =
        DOMPurify.sanitize(parsedMarkdown);


    // -----------------------------------
    // RAG Sources
    // -----------------------------------

    if (sources && sources.length > 0) {

        const sourcesContainer =
            document.createElement("div");

        sourcesContainer.className =
            "rag-sources";

        const sourceHeader =
            document.createElement("div");

        sourceHeader.className =
            "rag-sources-header";

        sourceHeader.innerHTML = `
            <div>
                <i class="fa-solid fa-book-open"></i>
                <span>Sources used</span>
            </div>

            <span class="source-count">
                ${sources.length}
            </span>
        `;

        sourcesContainer.appendChild(sourceHeader);


        const sourceList =
            document.createElement("div");

        sourceList.className =
            "rag-source-list";


        sources.forEach(source => {

            const sourceItem =
                document.createElement("div");

            sourceItem.className =
                "rag-source-item";


            const isAuthoritative =
                source.category === "authoritative";


            const displayName =
                source.filename
                    .replace(/\.(pdf|md|txt)$/i, "")
                    .replaceAll("_", " ");


            const categoryLabel =
                isAuthoritative
                    ? "Authoritative"
                    : "ProcureGuard Knowledge Base";


            const pageText =
                source.page !== null
                    ? ` · Page ${source.page}`
                    : "";


            sourceItem.innerHTML = `
                <div class="source-icon">
                    <i class="fa-solid ${
                        isAuthoritative
                            ? "fa-file-shield"
                            : "fa-brain"
                    }"></i>
                </div>

                <div class="source-details">

                    <div class="source-name"></div>

                    <div class="source-meta">
                        ${categoryLabel}${pageText}
                    </div>

                </div>
            `;

            sourceItem
                .querySelector(".source-name")
                .textContent = displayName;

            sourceList.appendChild(sourceItem);

        });


        sourcesContainer.appendChild(sourceList);

        messageElement
            .querySelector(".message-content")
            .appendChild(sourcesContainer);
    }


    chatMessages.appendChild(messageElement);
}

async function sendQuestion() {

    const question = investigatorInput.value.trim();

    if (!question) {
        return;
    }

    addUserMessage(question);

    investigatorInput.value = "";

    // Disable while request is processing
    investigatorInput.disabled = true;
    investigatorSendBtn.disabled = true;

    console.log("Sending to LLM:", {
        document_id: Number(documentId),
        question: question
    });

    try {

        const response = await fetch(
            "http://192.168.2.31:8000/llm/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    document_id: Number(documentId),
                    question: question
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                `LLM request failed: ${response.status}`
            );
        }

        const llmResponse = await response.json();

        console.log("LLM Response:", llmResponse);

        addAssistantMessage(llmResponse.answer, llmResponse.sources);

    }
    catch (error) {

        console.error(
            "AI Investigator Error:",
            error
        );

        addAssistantMessage(
        "Sorry, I couldn't complete the investigation. Please try again."
        );

    }
    finally {

        investigatorInput.disabled = false;
        investigatorSendBtn.disabled = false;

        investigatorInput.focus();

    }

}


// -----------------------------------
// Send button
// -----------------------------------

investigatorSendBtn.addEventListener(
    "click",
    sendQuestion
);


// -----------------------------------
// Press Enter to send
// -----------------------------------

investigatorInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendQuestion();

        }

    }
);