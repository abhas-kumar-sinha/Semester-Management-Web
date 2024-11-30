toggle = document.querySelector(".toggle");
sidebar = document.querySelector(".side-bar");
logout = document.querySelector(".nav-link-1");
courseAnalytics = document.querySelector(".course-analytics")
listSbOptions = document.querySelectorAll(".nav-link a")

async function fetchAtData() {
    try {
        coursesDataEle = document.querySelector("#courses").textContent;
        gradesDataEle = document.querySelector("#grades").textContent;

        coursesData = JSON.parse(coursesDataEle);
        gradesData = JSON.parse(gradesDataEle);

        if (coursesData.length == 0) {
            alertDiv = document.createElement('div')
            alertDiv.classList.add('alert-div')
            alertDiv.innerHTML += `
            <h1>No Courses To Display. </h1>
            <a href="Add-Course" class="sub-alert-div">
                <i class='bx bx-book-add'></i>
                <p>Add course</p>
            </a>`
            alertDiv.style.marginTop = `2.75vw`
            courseAnalytics.appendChild(alertDiv);
        } else{
            populategradesData(gradesData, coursesData);
        }


    } catch (error) {
        console.error("Error parsing data:", error);
    }
};

currPage = window.location.pathname;
listSbOptions[5].classList.add("is-active")
fetchAtData()

function giveGrade(yourTotal, finalTotal) {
    temp = (yourTotal/finalTotal)*100
    if (temp>80 && temp<100){
        return "A(10)"
    }else if(temp>70 && temp<80) {
        return "A(10) or A-(9)"
    }else if(temp>60 && temp<70) {
        return "A-(9) or B(8)"
    }else if(temp>50 && temp<60) {
        return "B(8) or B-(7)"
    }else if(temp>40 && temp<50) {
        return "B-(7) or C(6)"
    }else if(temp>30 && temp<40) {
        return "C(6) or C-(5)"
    }else if(temp>20 && temp<30) {
        return "D(4)"
    }else if(temp>10 && temp<20) {
        return "E-(2) Fail"
    }else if(temp>0 && temp<10) {
        return "F-(0) Fail"
    }else{
        return "some error occured while calculating"
    }
}

function giveGradeValue(yourTotal, finalTotal) {
    temp = (yourTotal/finalTotal)*100
    if (temp>80 && temp<100){
        return 10
    }else if(temp>70 && temp<80) {
        return 9
    }else if(temp>60 && temp<70) {
        return 8
    }else if(temp>50 && temp<60) {
        return 7
    }else if(temp>40 && temp<50) {
        return 6
    }else if(temp>30 && temp<40) {
        return 5
    }else if(temp>20 && temp<30) {
        return 4
    }else if(temp>10 && temp<20) {
        return 2
    }else if(temp>0 && temp<10) {
        return 0
    }else{
        return "some error occured while calculating"
    }
}

function populategradesData(gradesData, coursesData) {
    clacGradeBtnAll = document.querySelectorAll(".claculate-grade")
    clacGradeBtnAll.forEach(Btn => {
        Btn.addEventListener('click', () => {
            classArray = Btn.classList
            courseId = classArray[classArray.length - 2] + " " + classArray[classArray.length - 1]
            gradesData.forEach(data => {
                yourTotal = 0;
                finalTotal = 0;
                if (String(data[0]) === String(courseId)) {
                    for (key in data[1]) {
                        if (data[2][key] != "-") {
                            yourTotal+=parseFloat(data[2][key])
                            finalTotal+=parseFloat(data[1][key])
                        }
                    }
                    
                    expectedGrade = giveGrade(yourTotal, finalTotal)
                    alert(`Your Expected Grade in ${courseId} is ${expectedGrade}`)
                } 
            });
        });
    });
    sgpaBtn = document.querySelector(".sgpa-calc")
    sgpaBtn.addEventListener('click', () => {
        netUserTotal = 0;
        netFinalTotal = 0;
        gradesData.forEach(data => {
            coursesData.forEach(course => {
                if (String(data[0]) === String(course[0])) {
                    credits = parseInt(course[2])
                }
            });

            yourTotal = 0;
            finalTotal = 0;
            for (key in data[1]) {
                if (data[2][key] != "-") {
                    yourTotal+=parseFloat(data[2][key])
                    finalTotal+=parseFloat(data[1][key])
                }
            }
            
            if (finalTotal == 0){
                expectedGrade = 0
                credits = 0
            }
            else{
                expectedGrade = giveGradeValue(yourTotal, finalTotal)
            }
            
            netUserTotal+=expectedGrade*credits
            netFinalTotal+=credits

        });

        finalSgpa = netUserTotal/netFinalTotal
        finAns = Math.floor(finalSgpa * 100) / 100;
        alert(`Your Expected SGPA is ${finAns}`)
    })
};

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close")
})

sidebar.addEventListener('mouseenter', () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close") 
})

sidebar.addEventListener('mouseleave', () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close") 
})

addCourseBtn = document.querySelector(".add-button")
heroSection = document.querySelector(".hero-section")
courseForm = document.querySelector(".course-add-form")
closeForm = document.querySelector(".close-add-form")

addCourseBtn.addEventListener('click', () => {
    heroSection.classList.toggle("hide-feature")
    courseForm.classList.toggle("hide")
})

closeForm.addEventListener('click', () => {
    heroSection.classList.toggle("hide-feature")
    courseForm.classList.toggle("hide")
})

let addFieldBtn = document.querySelector(".add-field-btn");
let formTable = document.querySelector(".form-table");

let i = 4;

addFieldBtn.addEventListener("click", () => {
    i++;

    formTable.insertAdjacentHTML(
        "beforeend",
        `
        <tr>
            <td>
                <select class="form-input" name="assesment-type-${i}" id="form-course-type" required>
                    <option value="none" disabled selected>—————TYPE—————</option>
                    <option value="QUIZ - 1">QUIZ - 1</option>
                    <option value="QUIZ - 2">QUIZ - 2</option>
                    <option value="MINOR">MINOR</option>
                    <option value="MAJOR">MAJOR</option>
                    <option value="LAB">LAB</option>
                    <option value="TUTORIAL">TUTORIAL</option>
                    <option value="ASSIGNMENTS">ASSIGNMENTS</option>
                </select>
            </td>
            <td>
                <input type="text" class="form-input" name="assesment-weightage-${i}" id="form-course-name" required placeholder="Weightage (Out of 100)">
            </td>
        </tr>
        `
    );
});

inputFieldAll = document.querySelectorAll(".grade-input-1");
previousValue = ""; // Store the last valid value
previousCursorPosition = 0; // Store the last valid cursor position

inputFieldAll.forEach(inputField => {
    inputField.addEventListener("input", () => {
        const value = inputField.value;
        const cursorPosition = inputField.selectionStart;

        // Allow numbers with optional decimal points
        const isValid = /^-?\d*(\.\d*)?$/.test(value);

        if (isValid) {
            // Update previous values if valid character entered
            previousValue = value;
            previousCursorPosition = cursorPosition;
        } else {
            // Revert to previous valid state if invalid character entered
            inputField.value = previousValue;
            inputField.setSelectionRange(previousCursorPosition, previousCursorPosition);
        }
    });
});

inputFieldAll = document.querySelectorAll(".special-input-weightage");
previousValue = ""; // Store the last valid value
previousCursorPosition = 0; // Store the last valid cursor position

inputFieldAll.forEach(inputField => {
    inputField.addEventListener("input", () => {
        const value = inputField.value;
        const cursorPosition = inputField.selectionStart;

        // Allow numbers with optional decimal points
        const isValid = /^-?\d*(\.\d*)?$/.test(value);

        if (isValid) {
            // Update previous values if valid character entered
            previousValue = value;
            previousCursorPosition = cursorPosition;
        } else {
            // Revert to previous valid state if invalid character entered
            inputField.value = previousValue;
            inputField.setSelectionRange(previousCursorPosition, previousCursorPosition);
        }
    });
});
