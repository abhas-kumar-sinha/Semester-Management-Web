const inputField = document.getElementById("otp-input");
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