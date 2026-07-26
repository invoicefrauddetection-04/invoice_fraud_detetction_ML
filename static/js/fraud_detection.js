// ===================================
// ProcureGuard AI
// Fraud Detection
// ===================================

const input = document.getElementById("invoiceInput");
const browse = document.getElementById("browseBtn");
const preview = document.getElementById("previewContainer");

const stepUpload = document.getElementById("step-upload");
const stepProcessing = document.getElementById("step-processing");
const stepResult = document.getElementById("step-result");
const analyzeBtn = document.getElementById("analyzeBtn");


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

analyzeBtn.addEventListener("click", () => {

    processingCard.style.display = "block";

    stepProcessing.classList.add("active");

    const steps = [

        {
            text:"Reading invoice...",
            progress:20
        },

        {
            text:"Extracting invoice fields...",
            progress:40
        },

        {
            text:"Running fraud detection model...",
            progress:65
        },

        {
            text:"Calculating fraud probability...",
            progress:85
        },

        {
            text:"Generating explainability...",
            progress:100
        }

    ];

    let index = 0;

    const interval = setInterval(() => {

        processingStatus.textContent = steps[index].text;

        progressFill.style.width = steps[index].progress + "%";

        index++;

        if(index === steps.length){

    clearInterval(interval);

    stepResult.classList.add("active");

    processingStatus.textContent = "Analysis Complete ✔";

    // Show Prediction Card
    const predictionCard = document.getElementById("predictionCard");
    predictionCard.style.display = "block";

    // Fill Prediction Details
    document.getElementById("predictionBadge").textContent = "Fraud Detected";
    document.getElementById("confidenceValue").textContent = "96.42%";
    document.getElementById("riskLevel").textContent = "High";
    document.getElementById("invoiceId").textContent = "INV-2026-001";

}

    },1500);

});