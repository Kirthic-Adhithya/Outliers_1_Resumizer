// resumizer.js
function displayFileName(input) {
    const fileNameDisplay = document.getElementById("selected-file-name");
    if (input.files && input.files[0]) {
        fileNameDisplay.textContent = input.files[0].name;
    } else {
        fileNameDisplay.textContent = "";
    }
}

async function uploadResume() {
    const fileInput = document.getElementById("resume-file");
    const output = document.getElementById("output");
    const downloadLink = document.getElementById("download-link");
    const analysisSection = document.getElementById("analysis-section");

    if (!fileInput.files.length) {
        alert("Please upload a PDF file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    output.innerText = "Enhancing... Please wait.";
    downloadLink.style.display = "none";
    analysisSection.style.display = "none";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        
        if (data.error) {
            output.innerText = `Error: ${data.error}`;
            return;
        }

        // Store the resume text for later use
        window.resumeText = data.enhanced_resume;
        
        output.innerText = "Enhancement Complete! You can now download your resume.";
        downloadLink.href = data.download_url;
        downloadLink.style.display = "block";
        analysisSection.style.display = "block";

    } catch (error) {
        output.innerText = "Error processing your request. Please try again.";
        console.error("Upload error:", error);
    }
}

async function analyzeJobMatch() {
    const jobDescription = document.getElementById("job-description").value;
    const analysisOutput = document.getElementById("analysis-output");

    if (!jobDescription.trim()) {
        alert("Please enter a job description!");
        return;
    }

    if (!window.resumeText) {
        alert("Please upload and enhance a resume first!");
        return;
    }

    analysisOutput.innerText = "Analyzing... Please wait.";

    try {
        const response = await fetch("/analyze_job_match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                job_description: jobDescription,
                resume_text: window.resumeText
            })
        });

        const data = await response.json();

        if (data.error) {
            analysisOutput.innerText = `Error: ${data.error}`;
            return;
        }

        analysisOutput.innerHTML = data.analysis.replace(/\n/g, '<br>');
    } catch (error) {
        analysisOutput.innerText = "Error processing your request. Please try again.";
        console.error("Analysis error:", error);
    }
}