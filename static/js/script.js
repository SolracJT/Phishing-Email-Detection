const emailText =
    document.getElementById("emailText");

const characterCount =
    document.getElementById("characterCount");

const analyzeButton =
    document.getElementById("analyzeButton");

const clearButton =
    document.getElementById("clearButton");

const exampleButton =
    document.getElementById("exampleButton");

const resultStatus =
    document.getElementById("resultStatus");

const classification =
    document.getElementById("classification");


/* =========================================
   CHARACTER COUNTER
========================================= */

emailText.addEventListener("input", function () {

    characterCount.textContent =
        emailText.value.length;

});


/* =========================================
   RESET RESULT
========================================= */

function resetResult() {

    resultStatus.innerHTML =
        '<span class="result-status-dot"></span> Waiting';

    resultStatus.style.background =
        "#eeeeee";

    resultStatus.style.color =
        "#777777";

    classification.textContent =
        "No analysis yet";

    classification.className =
        "result-card-value";
}


/* =========================================
   CLEAR BUTTON
========================================= */

clearButton.addEventListener("click", function () {

    emailText.value = "";

    characterCount.textContent = "0";

    resetResult();

});


/* =========================================
   EXAMPLE BUTTON
========================================= */

exampleButton.addEventListener("click", function () {

    emailText.value =
        "Dear Customer,\n\n" +
        "Your account requires immediate verification. " +
        "Please confirm your account information by clicking " +
        "the verification link below. Failure to verify your " +
        "account within 24 hours may result in account suspension.\n\n" +
        "Thank you.";

    characterCount.textContent =
        emailText.value.length;

});


/* =========================================
   ANALYZE BUTTON
========================================= */

analyzeButton.addEventListener("click", function () {

    const email =
        emailText.value.trim();


    if (email === "") {

        resultStatus.innerHTML =
            '<span class="result-status-dot"></span> Input Required';

        resultStatus.style.background =
            "#fff0f0";

        resultStatus.style.color =
            "#d93f3f";

        classification.textContent =
            "No email content";

        classification.className =
            "result-card-value phishing";

        return;
    }


    /*
        Temporary frontend behavior.

        This will eventually be replaced with
        a request to the Flask backend.

        Example:

        fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email
            })
        })
        .then(response => response.json())
        .then(data => {

            classification.textContent =
                data.prediction;

        });
    */


    resultStatus.innerHTML =
        '<span class="result-status-dot"></span> Awaiting Model';

    resultStatus.style.background =
        "#fff4ef";

    resultStatus.style.color =
        "#ff6c37";

    classification.textContent =
        "Ready for Flask Model";

    classification.className =
        "result-card-value";

});