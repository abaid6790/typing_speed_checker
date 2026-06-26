// Elements
const paragraph = document.getElementById("paragraph");
const input = document.getElementById("input");
const timerElement = document.getElementById("timer");
const wpmElement = document.getElementById("wpm");
const accuracyElement = document.getElementById("accuracy");
const mistakesElement = document.getElementById("mistakes");
const difficultySelect =
document.getElementById("difficulty-select");
const timerSelect =
document.getElementById("timer-select");
// Variables
let timer = Number(duration);
let timeLeft = timer;
let timerStarted = false;
let interval = null;
let mistakes = 0;
let correctChars = 0;
let totalTyped = 0;
let finished = false;
// Highlight Paragraph
function renderParagraph() {
    paragraph.innerHTML = "";
    paragraphText.split("").forEach((char) => {
        const span = document.createElement("span");
        span.innerText = char;
        paragraph.appendChild(span);
    });
}
renderParagraph();
// Apply Settings
function applySettings() {
    const diff =
        difficultySelect.value;
    const time =
        timerSelect.value;
    window.location.href =
        `/typing?difficulty=${diff}&timer=${time}`;
}
// Start Timer
function startTimer() {
    if (timerStarted)
        return;
    timerStarted = true;
    interval = setInterval(() => {
        timeLeft--;
        timerElement.innerText = timeLeft;
        if (timeLeft <= 0) {
            finishTest();
        }
    }, 1000);
}
// Typing Event
input.addEventListener(
    "input",
    function () {
        if (!timerStarted)
            startTimer();
        if (finished)
            return;
        const typed =
            input.value;
        const spans =
            paragraph.querySelectorAll("span");
        mistakes = 0;
        correctChars = 0;
        totalTyped = typed.length;
        spans.forEach((span, index) => {
            const char =
                typed[index];
            span.className = "";
            if (char == null) {
                return;
            }
            if (char === span.innerText) {
                span.classList.add("correct");
                correctChars++;
            }
            else {
                span.classList.add("incorrect");
                mistakes++;
            }
        });
        updateStats();
        if (typed.length >= paragraphText.length) {
            finishTest();
        }
    }
);
// Statistics
function updateStats() {
    const elapsed =
        timer - timeLeft;
    let wpm = 0;
    if (elapsed > 0) {
        wpm = Math.round(
            (
                correctChars / 5
            )
            /
            (
                elapsed / 60
            )
        );
    }
    let accuracy = 100;
    if (totalTyped > 0) {
        accuracy = Math.round(
            (
                correctChars /
                totalTyped
            ) * 100
        );
    }
    wpmElement.innerText =
        wpm;
    accuracyElement.innerText =
        accuracy;
    mistakesElement.innerText =
        mistakes;
}
// Finish Test
function finishTest() {
    if (finished)
        return;
    finished = true;
    clearInterval(interval);
    input.disabled = true;
}
// Save Result
async function saveResult() {
    const wpm =
        Number(
            wpmElement.innerText
        );
    const accuracy =
        Number(
            accuracyElement.innerText
        );
    await fetch("/save-result", {
        method: "POST",
        headers: {
            "Content-Type":
            "application/json"
        },
        body: JSON.stringify({
            wpm: wpm,
            accuracy: accuracy,
            mistakes: mistakes,
            difficulty: difficulty,
            duration: timer
        })
    });
}
// Finish Test Override
const originalFinish = finishTest;
finishTest = async function () {
    if (finished)
        return;
    finished = true;
    clearInterval(interval);
    input.disabled = true;
    await saveResult();
    setTimeout(() => {
        alert(
            "🎉 Test Completed!"
        );
    }, 300);
};
// Restart Test
function restartTest() {
    location.reload();
}
// Prevent Copy
paragraph.addEventListener(
    "copy",
    function(e){
        e.preventDefault();
    }
);
// Prevent Paste
input.addEventListener(
    "paste",
    function(e){
        e.preventDefault();
        alert(
            "Paste is disabled."
        );
    }
);
// Prevent Right Click
document.addEventListener(
    "contextmenu",
    function(e){
        e.preventDefault();
    }
);
// Keyboard Shortcuts
document.addEventListener(
    "keydown",
    function(e){
        if(
            e.ctrlKey &&
            (
                e.key=="c" ||
                e.key=="v"
            )
        ){
            e.preventDefault();
        }
    }
);
// New Test
function newTest(){
    location.reload();
}
// Expose Functions
window.applySettings =
    applySettings;
window.restartTest =
    restartTest;
window.newTest =
    newTest;