// const paragraphs = {

//     easy_paragraphs = [
//     "Python is easy to learn and fun to use.",
//     "Practice typing every day to improve.",
//     "Coding helps solve real world problems.",
//     "Technology changes our lives every day.",
//     "Learning new skills builds confidence.",
//     "Artificial intelligence is becoming popular.",
//     "Programming requires patience and practice.",
//     "Computers help us perform tasks quickly.",
//     "Reading books improves knowledge and focus.",
//     "Typing speed increases with daily practice."
// ],
//     medium_paragraphs = [
//         "Machine learning enables systems to learn patterns from data without explicit programming.",
//         "Cloud computing provides scalable infrastructure over the internet for modern applications.",
//         "Data science combines statistics programming and domain knowledge to extract insights.",
//         "Python offers powerful libraries for automation machine learning and web development.",
//         "Cybersecurity professionals work to protect systems against unauthorized access and attacks.",
//         "Software engineering focuses on building reliable scalable and maintainable applications.",
//         "Computer vision enables machines to interpret and understand visual information.",
//         "Developers use version control systems to track changes in software projects.",
//         "Algorithms are essential for solving computational problems efficiently.",
//         "Artificial intelligence is transforming industries through automation and prediction."
// ],

//     hard_paragraphs = [
//         "Neural networks utilize interconnected computational layers to identify complex patterns within massive datasets.",
//         "Natural language processing enables machines to understand interpret and generate human language effectively.",
//         "Distributed systems require synchronization fault tolerance and scalability to maintain reliability under heavy workloads.",
//         "Advanced cybersecurity frameworks employ multiple defensive strategies to mitigate sophisticated threats.",
//         "Computer vision algorithms process high dimensional image data to extract meaningful representations.",
//         "Deep learning architectures achieve remarkable performance across diverse artificial intelligence applications.",
//         "Large scale software systems demand careful architectural planning testing and optimization.",
//         "Modern cloud platforms provide elastic resources capable of supporting millions of concurrent users.",
//         "Artificial intelligence continues to redefine business processes through intelligent automation and analytics.",
//         "Researchers continuously develop innovative algorithms to improve efficiency accuracy and scalability."
//     ]
// };

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

async function loadParagraph() {

    const level = difficulty.value;

    const response =
        await fetch(`/get-paragraph/${level}`);

    const data = await response.json();

    paragraph.textContent = data.paragraph;

    input.value = "";

    resetStats();
}

difficulty.addEventListener("change", loadParagraph);

function startTimer(){

    if(started) return;

    started = true;

    interval = setInterval(()=>{

        timer--;

        timeElement.textContent = timer;

        if(timer <= 0){

            finishTest();
        }

    },1000);
}

input.addEventListener("input", ()=>{

    startTimer();

    const typed = input.value;

    const original = paragraph.textContent;

    let mistakes = 0;

    for(let i=0;i<typed.length;i++){

        if(typed[i] !== original[i]){

            mistakes++;
        }
    }

    const progress =
        (typed.length/original.length)*100;

    progressBar.style.width =
        Math.min(progress,100)+"%";

    const elapsed =
        Math.max(1,(60-timer));

    const words =
        typed.trim().split(" ").length;

    const wpm =
        Math.round((words/elapsed)*60);

    const accuracy =
        Math.max(
            0,
            (((typed.length-mistakes)/
            Math.max(typed.length,1))*100)
        );

    wpmElement.textContent = wpm;
    accuracyElement.textContent =
        accuracy.toFixed(1)+"%";
    mistakesElement.textContent = mistakes;

    if(wpm > bestWpm){

        bestWpm = wpm;

        bestWpmElement.textContent =
            bestWpm;
    }

    if(typed.trim() === original.trim()){

        finishTest();
    }
});

function finishTest(){

    clearInterval(interval);

    started = false;

    let wpm =
        parseInt(wpmElement.textContent);

    let achievement =
        getAchievement(wpm);

    achievementElement.textContent =
        "Achievement: " + achievement;

    alert(
        `Test Complete!

WPM: ${wpm}

Achievement: ${achievement}`
    );
}

function getAchievement(wpm){

    if(wpm >= 100)
        return "🚀 Speed Demon";

    if(wpm >= 80)
        return "🥇 Fast Typist";

    if(wpm >= 60)
        return "🥈 Intermediate Typist";

    if(wpm >= 40)
        return "🥉 Beginner Typist";

    return "⌨ Keep Practicing";
}

function resetStats(){

    clearInterval(interval);

    timer = 60;

    started = false;

    timeElement.textContent = 60;

    progressBar.style.width = "0%";

    wpmElement.textContent = 0;
    accuracyElement.textContent = "100%";
    mistakesElement.textContent = 0;

    achievementElement.textContent =
        "Achievement: None";
}

document
.getElementById("restartBtn")
.addEventListener("click",()=>{

    loadParagraph();
});

document
.getElementById("newBtn")
.addEventListener("click",()=>{

    loadParagraph();
});

document
.getElementById("themeBtn")
.addEventListener("click",()=>{

    document.body.classList.toggle("dark");
});

input.addEventListener("paste",(e)=>{

    e.preventDefault();

    alert("Paste is not allowed!");
});