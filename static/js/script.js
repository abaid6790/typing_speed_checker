let timer = 60;
let interval = null;
let started = false;
let bestWpm = 0;
const paragraph = document.getElementById("paragraph");
const input = document.getElementById("typingInput");
const difficulty = document.getElementById("difficulty");
const timeElement = document.getElementById("time");
const progressBar = document.getElementById("progressBar");
const wpmElement = document.getElementById("wpm");
const accuracyElement = document.getElementById("accuracy");
const mistakesElement = document.getElementById("mistakes");
const bestWpmElement = document.getElementById("bestWpm");
const achievementElement = document.getElementById("achievement");
/* -----------------------------
   LOAD PARAGRAPH
----------------------------- */
async function loadParagraph() {
    const level = difficulty.value;
    try {
        const response = await fetch(
            `/get-paragraph/${level}`
        );
        const data = await response.json();
        paragraph.textContent = data.paragraph;
        input.value = "";
        resetStats();
    } catch (error) {
        console.error(error);
        paragraph.textContent =
            "Failed to load paragraph.";
    }
}
difficulty.addEventListener(
    "change",
    loadParagraph
);
/* -----------------------------
   TIMER
----------------------------- */
function startTimer() {
    if (started) return;
    started = true;
    interval = setInterval(() => {
        timer--;
        timeElement.textContent = timer;
        if (timer <= 0) {
            finishTest();
        }
    }, 1000);
}
/* -----------------------------
   LIVE TYPING
---------------------------- */
input.addEventListener("input", () => {
    startTimer();
    const typed = input.value;
    const original =
        paragraph.textContent;
    let mistakes = 0;
    for (
        let i = 0;
        i < typed.length;
        i++
    ) {
        if (
            typed[i] !== original[i]
        ) {
            mistakes++;
        }
    }
    const progress =
        (typed.length /
            original.length) *
        100;
    progressBar.style.width =
        Math.min(progress, 100) +
        "%";
    const elapsed =
        Math.max(
            1,
            60 - timer
        );
    const words =
        typed.trim()
            ? typed.trim().split(/\s+/)
                  .length
            : 0;
    const wpm = Math.round(
        (words / elapsed) * 60
    );
    const accuracy =
        Math.max(
            0,
            (
                ((typed.length -
                    mistakes) /
                    Math.max(
                        typed.length,
                        1
                    )) *
                100
            )
        );
    wpmElement.textContent = wpm;
    accuracyElement.textContent =
        accuracy.toFixed(1) + "%";
    mistakesElement.textContent =
        mistakes;
    if (wpm > bestWpm) {
        bestWpm = wpm;
        bestWpmElement.textContent =
            bestWpm;
    }
    if (
        typed.trim() ===
        original.trim()
    ) {
        finishTest();
    }
});
/* -----------------------------
   FINISH TEST
----------------------------- */
async function finishTest() {

    if(!started) return;

    clearInterval(interval);
    started = false;

    // rest of code...
}
async function finishTest() {
    clearInterval(interval);
    started = false;
    const wpm = parseInt(
        wpmElement.textContent
    );
    const accuracy =
        parseFloat(
            accuracyElement.textContent
        );
    const mistakes =
        parseInt(
            mistakesElement.textContent
        );
    const achievement =
        getAchievement(wpm);
    achievementElement.textContent =
        "Achievement: " +
        achievement;
    try {
        await fetch(
            "/save-result",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({
                    wpm: wpm,
                    accuracy: accuracy,
                    mistakes: mistakes,
                    difficulty: difficulty.value,
                    achievement: achievement
                })
            }
        );
    } catch (error) {
        console.log(
            "Database error:",
            error
        );
    }
    alert(
`Test Complete!
WPM: ${wpm}
Accuracy: ${accuracy}%
Mistakes: ${mistakes}
Achievement: ${achievement}`
    );
}
/* -----------------------------
   ACHIEVEMENTS
----------------------------- */
function getAchievement(wpm) {
    if (wpm >= 100)
        return "🚀 Speed Demon";
    if (wpm >= 80)
        return "🥇 Fast Typist";
    if (wpm >= 60)
        return "🥈 Intermediate Typist";
    if (wpm >= 40)
        return "🥉 Beginner Typist";
    return "⌨ Keep Practicing";
}
/* -----------------------------
   RESET
----------------------------- */
function resetStats() {
    clearInterval(interval);
    timer = 60;
    started = false;
    timeElement.textContent =
        "60";
    progressBar.style.width =
        "0%";
    wpmElement.textContent = "0";
    accuracyElement.textContent =
        "100%";
    mistakesElement.textContent =
        "0";
    achievementElement.textContent =
        "Achievement: None";
}
/* -----------------------------
   BUTTONS
----------------------------- */
document
    .getElementById(
        "restartBtn"
    )
    .addEventListener(
        "click",
        loadParagraph
    );
document
    .getElementById(
        "newBtn"
    )
    .addEventListener(
        "click",
        loadParagraph
    );
/* -----------------------------
   BLOCK PASTE
----------------------------- */
input.addEventListener(
    "paste",
    (e) => {
        e.preventDefault();
        alert(
            "Paste is not allowed!"
        );
    }
);
/* -----------------------------
   LOGOUT
----------------------------- */
const logoutBtn =
    document.getElementById(
        "logout-btn"
    );
if (logoutBtn) {
    logoutBtn.addEventListener(
        "click",
        () => {
            const confirmLogout =
                confirm(
                    "Are you sure you want to logout?"
                );
            if (
                !confirmLogout
            ) return;
            window.location.href =
                "/logout";
        }
    );
}
/* -----------------------------
   INITIAL LOAD
----------------------------- */
loadParagraph();