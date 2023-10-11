const email = document.querySelector('#email');
const username = document.querySelector('#username');
const emailFeedbackArea = document.querySelector(".email-feedback-area");
const usernameFeedbackArea = document.querySelector(".username-feedback-area");
const usernameSuccessOutput = document.querySelector(".username-success-output");
const submitBtn = document.querySelector('#submit-btn');

email.addEventListener('keyup', (e) => {
    const emailValue = e.target.value;

    emailFeedbackArea.style.display = "none";

    if (emailValue.length > 0) {
        fetch('/authentication/validate-email/', {
            body: JSON.stringify({ email: emailValue }),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data', data);
            if (data.email_exists) {
                submitBtn.setAttribute('disabled', 'true');
                email.classList.add("is-invalid");
                emailFeedbackArea.style.display = "block";
                emailFeedbackArea.innerHTML = `<p>${data.email_exists}</p>`;
            } else if (data.email_error) {
                submitBtn.setAttribute('disabled', 'true');
            } else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});

username.addEventListener('keyup', (e) => {
    const usernameValue = e.target.value;

    usernameSuccessOutput.textContent = `Validando ${usernameValue}`;
    usernameFeedbackArea.style.display = "none";

    if (usernameValue.length > 0) {
        fetch('/authentication/validate-username/', {
            body: JSON.stringify({ username: usernameValue }),
            method: 'POST',
        })
        .then((res) => res.json())
        .then((data) => {
            console.log('data', data);
            usernameSuccessOutput.style.display = 'none';
            if (data.username_exists) {
                submitBtn.setAttribute('disabled', 'true');
                username.classList.add("is-invalid");
                usernameFeedbackArea.style.display = "block";
                usernameFeedbackArea.innerHTML = `<p>${data.username_exists}</p>`;
            } else if (data.username_error) {
                submitBtn.setAttribute('disabled', 'true');
            } else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});