const wpmCtx =
document.getElementById(
    "wpmChart"
);

new Chart(wpmCtx, {

    type: "line",

    data: {

        labels: labels,

        datasets: [{

            label: "WPM",

            data: wpmData,

            tension: 0.4

        }]
    }
});


const accuracyCtx =
document.getElementById(
    "accuracyChart"
);

new Chart(accuracyCtx, {

    type: "line",

    data: {

        labels: labels,

        datasets: [{

            label: "Accuracy",

            data: accuracyData,

            tension: 0.4

        }]
    }
});