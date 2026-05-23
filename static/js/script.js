
// ---------------- REGISTER USER ----------------
async function registerUser() {

    const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/register", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            username: username,
            email: email,
            password: password
        })

    });

    const data = await response.json();

    alert(data.message);

}


// ---------------- LOGIN USER ----------------
async function loginUser() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            email: email,
            password: password
        })

    });

    const data = await response.json();

    // Save JWT token
    localStorage.setItem("token", data.token);

    alert(data.message);

    // Redirect to dashboard
    window.location.href = "/";

}


// ---------------- FETCH USER NOTES ----------------
async function fetchNotes() {

    const token = localStorage.getItem("token");

    const response = await fetch("/my-notes", {

        method: "GET",

        headers: {
            "Authorization": `Bearer ${token}`
        }

    });

    const data = await response.json();

    const notesContainer = document.getElementById("notes-container");

    notesContainer.innerHTML = "";

    data.notes.forEach(note => {

        notesContainer.innerHTML += `

            <div style="
                background:#0f172a;
                padding:15px;
                border-radius:10px;
                margin-bottom:15px;
            ">

                <h3>${note.title}</h3>

                <p>${note.content}</p>

            </div>

        `;

    });

}


// ---------------- ADD NOTE ----------------
async function addNote() {

    const title = document.getElementById("note-title").value;
    const content = document.getElementById("note-content").value;

    const token = localStorage.getItem("token");

    const response = await fetch("/add-note", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify({
            title: title,
            content: content
        })

    });

    const data = await response.json();

    alert(data.message);

    // Reload notes
    fetchNotes();

}


// ---------------- UPLOAD PDF ----------------
async function uploadPDF() {

    const pdfFile = document.getElementById("pdf-file").files[0];

    const token = localStorage.getItem("token");

    // Create form data
    const formData = new FormData();

    formData.append("pdf", pdfFile);

    const response = await fetch("/upload-pdf", {

        method: "POST",

        headers: {
            "Authorization": `Bearer ${token}`
        },

        body: formData

    });

    const data = await response.json();

    alert(data.message);

    // Automatically extract text
    extractPDFText(data.filename);

}


// ---------------- EXTRACT PDF TEXT ----------------
async function extractPDFText(filename) {

    const token = localStorage.getItem("token");

    const response = await fetch(`/extract-pdf-text/${filename}`, {

        method: "GET",

        headers: {
            "Authorization": `Bearer ${token}`
        }

    });

    const data = await response.json();

    console.log(data.extracted_text);

    // Show extracted PDF text
    document.getElementById("summary-box").value =
        data.extracted_text;

    alert("PDF Text Extracted Successfully 🚀");

}

