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
const API_URL = "http://192.168.1.208:8000/upload";


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

// analyzeBtn.addEventListener("click", async () => {

//     const file = input.files[0];

//     if (!file) {
//         alert("Please select an invoice.");
//         return;
//     }

//     processingCard.style.display = "block";

//     stepProcessing.classList.add("active");

//     processingStatus.textContent = "Uploading Invoice...";

//     progressFill.style.width = "10%";

//     const formData = new FormData();

//     formData.append("file", file);

//     try {

//         const response = await fetch(API_URL, {

//             method: "POST",

//             body: formData

//         });

//         if (!response.ok) {

//             throw new Error("Upload Failed");

//         }

//         const data = await response.json();

//         console.log(data);

//         processingStatus.textContent = "Processing Invoice...";

//         progressFill.style.width = "100%";

//         stepResult.classList.add("active");

//         processingStatus.textContent = "Completed ✔";

//         console.log(data);

//     }

//     catch(error){

//         console.error(error);

//         processingStatus.textContent = "Upload Failed";

//     }

// });

// analyzeBtn.addEventListener("click", async () => {

//     const file = input.files[0];

//     if (!file) {
//         alert("Please select a file");
//         return;
//     }

//     const formData = new FormData();
//     formData.append("file", file);

//     try {

//         const response = await fetch("http://192.168.1.208:8000/upload", {
//             method: "POST",
//             body: formData
//         });

//         const data = await response.json();

//         console.log("Backend Response:", data);

//         alert("Upload Successful");

//     } catch (err) {

//         console.error(err);

//         alert("Upload Failed");

//     }
// });

// Backend URL
const API_BASE_URL = "http://192.168.1.208:8000";

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

        // -----------------------------
        // Upload Successful
        // -----------------------------
        processingCard.style.display = "block";

        stepProcessing.classList.add("active");

        const steps = [

            {
                text: "Uploading invoice...",
                progress: 15
            },

            {
                text: "Converting PDF to Images...",
                progress: 35
            },

            {
                text: "Extracting invoice fields...",
                progress: 55
            },

            {
                text: "Running Fraud Detection...",
                progress: 80
            },

            {
                text: "Generating Results...",
                progress: 100
            }

        ];

        let index = 0;

        const interval = setInterval(() => {

            processingStatus.textContent = steps[index].text;

            progressFill.style.width =
                steps[index].progress + "%";

            index++;

            if (index === steps.length) {

                clearInterval(interval);

                stepResult.classList.add("active");

                processingStatus.textContent =
                    "Analysis Complete ✔";

                const predictionCard =
                    document.getElementById("predictionCard");

                predictionCard.style.display = "block";

                // Temporary values
                document.getElementById("predictionBadge").textContent =
                    "Processing Completed";

                document.getElementById("confidenceValue").textContent =
                    "100%";

                document.getElementById("riskLevel").textContent =
                    "Pending ML";

                document.getElementById("invoiceId").textContent =
                    data.filename;

            }

        }, 1200);

    }
    catch (error) {

        console.error(error);

        alert("Unable to upload invoice.");

    }
    finally {

        analyzeBtn.disabled = false;

    }

});


