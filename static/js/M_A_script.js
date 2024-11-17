async function fetchAtData() {
    try {
        // Get the text content of the element with ID "attendance"
        coursesDataEle = document.querySelector("#courses").textContent;
        timetableDataEle = document.querySelector("#timetables_list").textContent;

        // Parse JSON data
        coursesData = JSON.parse(coursesDataEle);
        timetableData = JSON.parse(timetableDataEle);

        // Now, populate the form using this data
        populateCourseOptions1(coursesData);
        populateCourseOptions2(timetableData);

    } catch (error) {
        temp=1;
    }
};

fetchAtData();

function populateCourseOptions1(coursesData) {}

function populateCourseOptions2(timetableData) {}

submitBtnsAll = document.querySelectorAll(".marked-att");

submitBtnsAll.forEach(element => {
    element.addEventListener('submit', () => {
        element.disabled = true;
        element.innerText = `Submitted`;
    })
});