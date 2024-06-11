async function postData(url = "", data = {}) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return response.json();
}

document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("sendButton");
    const questionInput = document.getElementById("questioninput");
    const right1 = document.querySelector(".right1");
    const right2 = document.querySelector(".right2");
    const question1 = document.getElementById("question1");
    const question2 = document.getElementById("question2");
    const solution = document.getElementById("solution");

    sendButton.addEventListener("click", async () => {
        const question = questionInput.value.trim();
        if (question) {
            questionInput.value = "";
            right1.style.display = "none";
            right2.style.display = "flex";
            question1.innerHTML = question;
            question2.innerHTML = question;
            solution.innerHTML = "Loading...";

            try {
                const result = await postData("/api", { question: question });
                solution.innerHTML = result.result;
            } catch (error) {
                solution.innerHTML = "Error: Unable to fetch the answer.";
                console.error("Error:", error);
            }
        }
    });
});
