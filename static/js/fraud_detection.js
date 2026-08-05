// ===================================
// ProcureGuard AI
// Fraud Detection
// ===================================

let currentDocumentId = null;

const input = document.getElementById("invoiceInput");
const browse = document.getElementById("browseBtn");
const preview = document.getElementById("previewContainer");

const stepUpload = document.getElementById("step-upload");
const stepProcessing = document.getElementById("step-processing");
const stepResult = document.getElementById("step-result");
const analyzeBtn = document.getElementById("analyzeBtn");

// const API_URL = "http://192.168.2.214:8000/upload";

async function waitForPrediction(imageName) {

    while (true) {

        const response = await fetch(
            `${API_BASE_URL}/prediction/${imageName}`
        );

        const prediction = await response.json();

        console.log(prediction);

        if (prediction.status === "success") {

            return prediction;

        }

        await new Promise(resolve => setTimeout(resolve, 3000));

    }

}


browse.addEventListener("click", () => {

    input.click();

});

input.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    stepUpload.classList.add("active");
    stepProcessing.classList.remove("active");
    stepResult.classList.remove("active");

    if (file.type.startsWith("image/")) {

        const img = document.createElement("img");

        img.src = URL.createObjectURL(file);

        img.style.width = "100%";

        img.style.height = "100%";

        img.style.objectFit = "contain";

        img.style.borderRadius = "12px";

        preview.innerHTML = "";

        preview.appendChild(img);

    }

    else {

        preview.innerHTML = `
            <div class="preview-placeholder">

                <i class="fa-solid fa-file-pdf"></i>

                <h3>${file.name}</h3>

                <p>PDF Uploaded Successfully</p>

            </div>
        `;

    }

});

input.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) return;

    // Enable Analyze button
    analyzeBtn.disabled = false;

    // Update workflow
    stepUpload.classList.add("active");
    stepProcessing.classList.remove("active");
    stepResult.classList.remove("active");

    if (file.type.startsWith("image/")) {

        const img = document.createElement("img");

        img.src = URL.createObjectURL(file);

        img.style.width = "100%";

        img.style.borderRadius = "12px";

        preview.innerHTML = "";

        preview.appendChild(img);

    }

    else {

        preview.innerHTML = `
            <div class="preview-placeholder">
                <i class="fa-solid fa-file-pdf"></i>
                <h3>${file.name}</h3>
                <p>PDF Uploaded Successfully</p>
            </div>
        `;

    }

});

const processingCard = document.getElementById("processingCard");
const processingStatus = document.getElementById("processingStatus");
const progressFill = document.getElementById("progressFill");

// Backend URL
// change the IP here to your backend server's IP address
const API_BASE_URL = "http://192.168.1.184:8000";

const processingMessages = [

    "Processing...",

    "Please wait...",

    "Analyzing invoice...",

    "Still processing...",

    "Preparing results..."

];


analyzeBtn.addEventListener("click", async () => {

    const file = input.files[0];

    if (!file) {
        alert("Please select an invoice.");
        return;
    }

    analyzeBtn.disabled = true;


    const formData = new FormData();
    formData.append("file", file);

    try {

        // -----------------------------
        // Upload invoice to backend
        // -----------------------------
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Upload Failed");
        }

        const data = await response.json();

        console.log("Backend Response:", data);

        const imageName = data.image_name;

        // Start polling backend immediately (runs in parallel)
        const predictionPromise = waitForPrediction(imageName);

        // -----------------------------
        // Upload Successful
        // -----------------------------
        processingCard.style.display = "block";

        stepProcessing.classList.add("active");

        let progress = 10;
    let msgIndex = 0;

    processingStatus.textContent = processingMessages[0];
    progressFill.style.width = progress + "%";

    const interval = setInterval(() => {

    // Change message
    processingStatus.textContent =
        processingMessages[msgIndex];

    if (msgIndex < processingMessages.length - 1) {
        msgIndex++;
    }

    // Slowly increase progress but stop at 90%
    if (progress < 90) {

        progress += Math.random() * 8;

        if (progress > 90)
            progress = 90;

        progressFill.style.width = progress + "%";

    }

}, 2500);

        const prediction = await predictionPromise;


        // Save document ID of current invoice
        currentDocumentId = prediction.document_id;

        console.log("Current Document ID:", currentDocumentId);

        localStorage.setItem(
        "currentDocumentId",
        currentDocumentId
        );

        clearInterval(interval);

        progressFill.style.width = "100%";

        processingStatus.textContent =
            "Analysis Complete ✔";

        stepResult.classList.add("active");

        const predictionCard =
    document.getElementById("predictionCard");

        predictionCard.style.display = "block";

        // document.getElementById("predictionBadge").textContent =
        //     prediction.prediction;

        const predictionBadge =
            document.getElementById("predictionBadge");

        predictionBadge.textContent = prediction.prediction;

        // Remove previous prediction colors
        predictionBadge.classList.remove("fraud", "genuine");

        // Apply color according to model prediction
        if (prediction.prediction.toLowerCase() === "fraud") {

            predictionBadge.classList.add("fraud");

        } else {

            predictionBadge.classList.add("genuine");

        }

        const confidence =
            (prediction.fraud_probability * 100).toFixed(2);

        document.getElementById("confidenceValue").textContent =
            confidence + "%";

        let risk;

        if (prediction.fraud_probability >= 0.80)
            risk = "High";
        else if (prediction.fraud_probability >= 0.40)
            risk = "Medium";
        else
            risk = "Low";

        document.getElementById("riskLevel").textContent =
            risk;

        document.getElementById("invoiceId").textContent =
            data.filename;

        analyzeBtn.disabled = false;

    }
    catch (error) {

        console.error(error);

        alert("Unable to upload invoice.");

    }
    finally {

    }

});


