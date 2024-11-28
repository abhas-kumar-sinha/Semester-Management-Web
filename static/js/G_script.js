toggle = document.querySelector(".toggle");
sidebar = document.querySelector(".side-bar");
logout = document.querySelector(".nav-link-1");
courseAnalytics = document.querySelector(".course-analytics")
listSbOptions = document.querySelectorAll(".nav-link a")

async function fetchAtData() {
    try {
        attendanceDataEle = document.querySelector("#attendance").textContent;
        gradesDataEle = document.querySelector("#grades").textContent;

        attendanceData = JSON.parse(attendanceDataEle);
        gradesData = JSON.parse(gradesDataEle);

        if (attendanceData.length == 0) {
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
            populategradesData(gradesData);
        }


    } catch (error) {
        temp=1;
    }
};

currPage = window.location.pathname;
listSbOptions[5].classList.add("is-active")
fetchAtData()

function populategradesData(gradesData) {
    clacGradeBtnAll = document.querySelectorAll(".claculate-grade")
    clacGradeBtnAll.forEach(Btn => {
        Btn.addEventListener('click', () => {
            classArray = Btn.classList
            courseId = classArray[classArray.length - 2] + " " + classArray[classArray.length - 1]
            gradesData.forEach(data => {
                ans = 0
                if (String(data[0]) === String(courseId)) {
                    for (key in data[1]) {
                        ans += parseFloat(data[2][key])
                    }

                    alert(`Your Expected Grade in ${courseId} is ${ans}`)
                } 
            });
        });
    });
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
editBtn = document.querySelector(".edit-button")
listCourseDel = document.querySelectorAll(".course-delete")

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
                    <option value="none">—————TYPE—————</option>
                    <option value="QUIZ - 1">QUIZ - 1</option>
                    <option value="QUIZ - 2">QUIZ - 2</option>
                    <option value="MINOR">MINOR</option>
                    <option value="MAJOR">MAJOR</option>
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