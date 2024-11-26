listOfButtons = document.querySelectorAll(".button")
togglePassword = document.querySelector(".show-hide-password")
passwordField = document.querySelector(".form-password")

listOfButtons.forEach(button => {
    button.addEventListener('click', () => {
        const req_id = prompt(`Enter your ${button.classList[0]} I'd`);
        if (req_id == "") {
            window.alert(`Sign In failed! Invalid ${button.classList[0]} I'd`)
        }
        else if (req_id != null){
            const req_id_pass = prompt(`Enter your ${button.classList[0]} Password`);
            if (req_id_pass == "") {
                window.alert(`Sign In failed! Invalid ${button.classList[0]} Password`)
            }
            else if (req_id_pass != null){
                window.alert(`Successfully registered using ${button.classList[0]} credentials`)
            }
            else {
                window.alert("cancelled")
            }
        }
        else {
            window.alert("cancelled")
        }
    })    
});

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