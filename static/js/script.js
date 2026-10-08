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
   TOAST
========================================= */

let toastTimer = null;

function showToast(message, type = "") {

    const existingToast =
        document.querySelector(".toast");

    if (existingToast) {
        existingToast.remove();
    }

    const toast =
        document.createElement("div");

    toast.className =
        `toast ${type}`;

    toast.textContent =
        message;

    document.body.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add("show");
    });

    clearTimeout(toastTimer);

    toastTimer =
        setTimeout(() => {

            toast.classList.remove("show");

            setTimeout(() => {
                toast.remove();
            }, 250);

        }, 2800);
}


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

    classification.parentElement.classList.remove(
        "result-success",
        "result-danger"
    );
}


/* =========================================
   CLEAR BUTTON
========================================= */

clearButton.addEventListener("click", function () {

    emailText.value = "";

    characterCount.textContent = "0";

    resetResult();

    showToast(
        "Email input cleared.",
        ""
    );

    emailText.focus();

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

    resetResult();

    showToast(
        "Example phishing email loaded.",
        ""
    );

    emailText.focus();

});


/* =========================================
   ANALYZE BUTTON
========================================= */

analyzeButton.addEventListener(
    "click",
    async function () {

        const email =
            emailText.value.trim();


        /* Empty input */

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

            showToast(
                "Please enter an email before analyzing.",
                "error"
            );

            emailText.focus();

            return;
        }


        /* Loading state */

        analyzeButton.disabled = true;

        analyzeButton.innerHTML =
            '<span class="button-loader"></span> Analyzing...';


        resultStatus.innerHTML =
            '<span class="result-status-dot"></span> Analyzing';

        resultStatus.style.background =
            "#fff4ef";

        resultStatus.style.color =
            "#ff6c37";

        classification.textContent =
            "Analyzing email...";

        classification.className =
            "result-card-value";


        try {

            const response =
                await fetch("/predict", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: email
                    })

                });


            const data =
                await response.json();


            if (!response.ok) {
                throw new Error(
                    data.error || "Prediction failed."
                );
            }


            /* =====================================
               PHISHING RESULT
            ===================================== */

            if (
                data.prediction ===
                "Phishing Email"
            ) {

                classification.textContent =
                    "Phishing Email";

                classification.className =
                    "result-card-value phishing result-reveal";


                resultStatus.innerHTML =
                    '<span class="result-status-dot"></span> Phishing Detected';

                resultStatus.style.background =
                    "#fff0f0";

                resultStatus.style.color =
                    "#d93f3f";


                resultStatus
                    .querySelector(".result-status-dot")
                    .style.background =
                    "#d93f3f";


                classification.parentElement
                    .classList.add("result-danger");


                resultStatus.classList.add(
                    "result-pulse"
                );


                showToast(
                    "Analysis complete: phishing detected.",
                    "error"
                );


            }

            /* =====================================
               SAFE RESULT
            ===================================== */

            else {

                classification.textContent =
                    "Safe Email";

                classification.className =
                    "result-card-value legitimate result-reveal";


                resultStatus.innerHTML =
                    '<span class="result-status-dot"></span> No Threat Detected';

                resultStatus.style.background =
                    "#eef9f1";

                resultStatus.style.color =
                    "#16883e";


                resultStatus
                    .querySelector(".result-status-dot")
                    .style.background =
                    "#16883e";


                classification.parentElement
                    .classList.add("result-success");


                resultStatus.classList.add(
                    "result-pulse"
                );


                showToast(
                    "Analysis complete: email appears safe.",
                    "success"
                );

            }


            /* Remove animation classes after animation */

            setTimeout(() => {

                classification.classList.remove(
                    "result-reveal"
                );

                resultStatus.classList.remove(
                    "result-pulse"
                );

            }, 600);


        } catch (error) {

            console.error(error);


            resultStatus.innerHTML =
                '<span class="result-status-dot"></span> Error';

            resultStatus.style.background =
                "#fff0f0";

            resultStatus.style.color =
                "#d93f3f";


            classification.textContent =
                "Unable to analyze email";

            classification.className =
                "result-card-value phishing";


            classification.parentElement
                .classList.add("result-danger");


            showToast(
                "Unable to connect to the detection model.",
                "error"
            );

        } finally {

            analyzeButton.disabled = false;

            analyzeButton.innerHTML =
                "Analyze Email";

        }

    }
);