const availableKeywords = [
    'Account Details',
    'Theme',
    'Notifications',
    'Reminders',
    'Info',
    'Reset Data',
    'Delete Account'
];

const inputBox = document.querySelector('.search-input');
const resultBox = document.querySelector('.result-box');

resultBox.style.display = "none";

inputBox.onkeyup = function() {
    resultBox.style.display = "";
    let result = [];
    let input = inputBox.value;

    if (input.length) {
        result = availableKeywords.filter(keyword => 
            keyword.toLowerCase().includes(input.toLowerCase())
        );
    }
    display(result);
};

function display(result) {
    if (result.length === 0) {
        resultBox.style.display = "none"; // Hide the result box when no results are found
        return;
    }

    const content = result.map(list => 
        `<li onclick=selectInput(this)>${list}</li>`
    ).join('');

    resultBox.innerHTML = `<ul style="list-style-type: none;">${content}</ul>`;
}

function selectInput(list){
    inputBox.value = list.innerHTML;
    resultBox.innerHTML = ``;
    resultBox.style.display = "none";
}