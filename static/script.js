// =========================================================
// STUDYSPACE AI — FRONTEND LOGIC
// =========================================================


// =========================================================
// ELEMENTS
// =========================================================

const questionInput = document.getElementById("questionInput");
const askButton = document.getElementById("askButton");

const answerSection = document.getElementById("answerSection");
const answerContent = document.getElementById("answerContent");
const sourcesContent = document.getElementById("sourcesContent");

const suggestionButtons =
    document.querySelectorAll(".suggestion");


// =========================================================
// ASK QUESTION
// =========================================================

async function askQuestion(question) {

    question = question.trim();

    if (!question) {

        questionInput.focus();

        return;
    }


    // Show answer section
    answerSection.classList.add("visible");


    // Loading state
    answerContent.innerHTML = `
        <p class="loading">
            Thinking...
        </p>
    `;


    sourcesContent.innerHTML = `
        <p class="loading">
            Finding relevant chapters...
        </p>
    `;


    // Disable button
    askButton.disabled = true;

    askButton.querySelector("span:first-child").textContent =
        "THINKING";


    try {

        const response = await fetch(
            "/api/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );


        // Handle server error
        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );
        }


        const data = await response.json();


        // Display answer
        displayAnswer(data.answer);


        // Display sources
        displaySources(data.sources);


        // Scroll to answer
        setTimeout(() => {

            answerSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }, 100);


    } catch (error) {

        console.error(error);


        answerContent.innerHTML = `
            <p class="error-message">
                Something went wrong while getting your answer.
                Please make sure the FastAPI server is running.
            </p>
        `;


        sourcesContent.innerHTML = `
            <p class="empty-sources">
                No sources available.
            </p>
        `;

    } finally {

        // Enable button again
        askButton.disabled = false;

        askButton.querySelector("span:first-child").textContent =
            "ASK AI";
    }
}


// =========================================================
// DISPLAY ANSWER
// =========================================================

function displayAnswer(answer) {

    if (!answer) {

        answerContent.innerHTML = `
            <p class="error-message">
                No answer was returned.
            </p>
        `;

        return;
    }


    /*
        Convert simple line breaks into paragraphs.
    */

    const paragraphs = answer
        .split(/\n+/)
        .map(text => text.trim())
        .filter(text => text.length > 0);


    answerContent.innerHTML = paragraphs
        .map(paragraph => {

            return `<p>${escapeHTML(paragraph)}</p>`;

        })
        .join("<br>");
}


// =========================================================
// DISPLAY SOURCES
// =========================================================

function displaySources(sources) {

    if (!sources || sources.length === 0) {

        sourcesContent.innerHTML = `
            <p class="empty-sources">
                No sources were returned.
            </p>
        `;

        return;
    }


    sourcesContent.innerHTML = "";


    sources.forEach((source, index) => {

        const sourceItem =
            document.createElement("div");

        sourceItem.className = "source-item";


        sourceItem.innerHTML = `

            <span class="source-name">
                ${index + 1}.
                ${escapeHTML(source.source)}
            </span>

            <span class="source-page">
                PAGE ${source.page}
            </span>

        `;


        sourcesContent.appendChild(
            sourceItem
        );

    });
}


// =========================================================
// SUGGESTED QUESTIONS
// =========================================================

suggestionButtons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            const question =
                button.dataset.question;


            questionInput.value =
                question;


            questionInput.focus();


            // Move user to question box
            questionInput.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });

        }
    );

});


// =========================================================
// ASK BUTTON
// =========================================================

askButton.addEventListener(
    "click",
    () => {

        askQuestion(
            questionInput.value
        );

    }
);


// =========================================================
// ENTER KEY
// =========================================================

questionInput.addEventListener(
    "keydown",
    (event) => {

        /*
            Ctrl + Enter / Enter
            can submit the question.

            Shift + Enter creates a new line.
        */

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            askQuestion(
                questionInput.value
            );

        }

    }
);


// =========================================================
// HTML ESCAPE
// =========================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}