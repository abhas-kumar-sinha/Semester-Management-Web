listOfButtons = document.querySelectorAll(".button")

listOfButtons.forEach(button => {
    button.addEventListener('click', () => {
        const req_id = prompt(`Enter your ${button.classList[0]} I'd`);
        console.log(req_id)
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