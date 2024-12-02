togglePassword = document.querySelector(".show-hide-password")
passwordField = document.querySelector(".form-password")

togglePassword.addEventListener('click', () => {
    condition = passwordField.getAttribute('type')

    if (condition.toLowerCase() === "password") {
        togglePassword.innerHTML = `<i class='bx bx-show' ></i>`
        passwordField.setAttribute('type', 'TEXT')
    } else{
        togglePassword.innerHTML = `<i class='bx bx-hide' ></i>`
        passwordField.setAttribute('type', 'PASSWORD')
    }
});

const inputField = document.getElementById("year-of-joining");
let previousValue = ""; // Store the last valid value
let previousCursorPosition = 0; // Store the last valid cursor position

inputField.addEventListener("input", () => {
    const value = inputField.value;
    const cursorPosition = inputField.selectionStart;

    // Only allow alphabetic characters
    const isValid = /^[0-9]*$/.test(value);

    if (isValid) {
        // Update previous values if valid character entered
        previousValue = value;
        previousCursorPosition = cursorPosition;
    } else {
        // Revert to previous valid state if invalid character entered
        inputField.value = previousValue;
    }
});