const availableKeywords = [
    'Account Details',
    'Theme',
    'Notifications',
    'Reminders',
    'Info',
    'Reset Data',
    'Delete Account',
    'Profile Photo',
    'User Name',
    'Email',
    'Number of Courses', 
    'Appearance',
    'light mode',
    'dark mode',
    'SGPA Leaderboard'
];

const inputBox = document.querySelector('.search-input');
const resultBox = document.querySelector('.result-box');

resultBox.style.display = "none";

inputBox.onkeyup = function() {
    resultBox.style.display = "";
    inputBox.addEventListener('focus', () => {
        resultBox.style.display = "";
    });

    inputBox.addEventListener('blur', () => {
        document.addEventListener('click', (event) => {
            if (resultBox.contains(event.target)) {

                console.log("ResultBox clicked");

            } else if (inputBox.contains(event.target)) {

                console.log("InputBox clicked");

            } else {

                console.log("Clicked outside");
                resultBox.style.display = "none";
            }
        })
    });
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
        resultBox.style.display = "none";
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

downSliderAll = document.querySelectorAll(".box-top")

downSliderAll.forEach(slider => {
    slider.addEventListener('click', () => {
        sliderType = slider.id
        reqEle = document.querySelector(`#${sliderType}`)
        reqEle.classList.toggle(sliderType)
    })
});

to_test = window.location.hash

if (to_test == "#Grades") {
    hero = document.querySelector("#Grades")
    hero.classList.add("Grades")
}
