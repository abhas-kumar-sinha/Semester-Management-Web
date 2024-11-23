addCourseBtn = document.querySelector(".add-button")
heroSection = document.querySelector(".hero-section")
courseForm = document.querySelector(".course-add-form")
closeForm = document.querySelector(".close-add-form")
editBtn = document.querySelector(".edit-button")
listCourseDel = document.querySelectorAll(".course-delete")

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

function populateCourseOptions1(coursesData) {
    let courseOptions = '';

    coursesData.forEach(course => {
        courseOptions += `<option value="${course[0]}">${course[0]}</option>`;
    });

    mainBtn = document.querySelector(".add-in-form")
    idx=0
    mainBtn.addEventListener('click', () => {
        addition = document.querySelector(".add-in-form")
        container = document.querySelector(".form-wrapper")
        idx++;
        // Now set the innerHTML using the dynamic `courseOptions` string
        const innerContainer = document.createElement('div');
        innerContainer.classList.add("in-forms")
        innerContainer.innerHTML = `
            <div class="form-separator" style="margin-top: 3vw;">
                <div class="line-div"></div>
                <span>Course Details</span>
                <div class="line-div"></div>
            </div>

            <table class="form-table">
                <tr>
                    <td><label class="form-label" for="form-course-name">Course Name</label></td>
                    <td><select class="form-input" name="course-id-${idx}" id="form-course-name" required>
                        <option value="none">—————SELECT—————</option>
                        ${courseOptions}  <!-- Dynamically added options here -->
                    </select></td>
                </tr>
                <tr>
                    <td><label class="form-label" for="form-course-type">Class Type</label></td>
                    <td><select class="form-input" name="class-type-${idx}" id="form-course-type" required>
                        <option value="none">—————SELECT—————</option>
                        <option value="LECTURE">LECTURE</option>
                        <option value="TUTORIAL">TUTORIAL</option>
                        <option value="INTRODUCTION">INTRODUCTION</option>
                        <option value="LAB">LAB</option>
                    </select></td>
                </tr>
                <tr>
                    <td><label class="form-label" for="form-day">Day</label></td>
                    <td><select class="form-input" name="day-${idx}" id="form-day" required>
                        <option value="none">—————SELECT—————</option>
                        <option value="MON">MON</option>
                        <option value="TUE">TUE</option>
                        <option value="WED">WED</option>
                        <option value="THUR">THUR</option>
                        <option value="FRI">FRI</option>
                    </select></td>
                </tr>
                <tr>
                    <td><label class="form-label" for="form-start-time">Class Start Time</label></td>
                    <td><select class="form-input start-time" name="class-start-time-${idx}" id="form-start-time" required>
                        <option value="none">—————SELECT—————</option>
                        <option value="8:00 AM">8:00 AM</option>
                        <option value="9:00 AM">9:00 AM</option>
                        <option value="10:00 AM">10:00 AM</option>
                        <option value="11:00 AM">11:00 AM</option>
                        <option value="12:00 PM">12:00 PM</option>
                        <option value="1:00 PM">1:00 PM</option>
                        <option value="2:00 PM">2:00 PM</option>
                        <option value="3:00 PM">3:00 PM</option>
                        <option value="4:00 PM">4:00 PM</option>
                        <option value="5:00 PM">5:00 PM</option>
                    </select></td>
                </tr>
                <tr>
                    <td><label class="form-label" for="form-end-time">Class End Time</label></td>
                    <td><select class="form-input end-time" name="class-end-time-${idx}" id="form-end-time" required>
                        <!-- Dynamic end time options can go here -->
                    </select></td>
                </tr>
            </table>
        `;

        // Append the populated innerContainer to the main container
        container.appendChild(innerContainer);
    });
}

function populateCourseOptions2(timetableData) {
    timeMap = {"8:00 AM" : "2", "9:00 AM" : "3", "10:00 AM" : "4", "11:00 AM" : "5", "12:00 PM" : "6", "1:00 PM" : "7", "2:00 PM" : "8", "3:00 PM" : "9", "4:00 PM" : "10", "5:00 PM" : "11", "6:00 PM" : "12"}

    dayMap = {"MON" : "2", "TUE" : "3", "WED" : "4", "THUR" : "5", "FRI" : "6"}
    timetableData.forEach(timetable => {
        DivContainer = document.querySelector(".front-view")
        newDiv = document.createElement('div')
        if (timetable.class_type == "LECTURE") {
            newDiv.classList.add("LECTURE");
        }
        else if(timetable.class_type == "TUTORIAL") {
            newDiv.classList.add("TUTORIAL");
        }
        else if(timetable.class_type == "INTRODUCTION"){
            newDiv.classList.add("INTRODUCTION");
        }
        else if(timetable.class_type == "LAB"){
            newDiv.classList.add("LAB");
        }

        day = timetable.day;
        startTime = timetable.start_time;
        endTime = timetable.end_time;
        endSpan = parseInt(timeMap[endTime]);
        finalEndSpan = String(endSpan)
        newDiv.innerHTML+= `
        <div class="delete-course-form hide">
            <form action="/Today-Schedule" method='POST'>
                <input style="display:none;" name="form-name" value="delete-course">
                <input style="display:none;" name="course-id" value="${timetable.course_id}">
                <input style="display:none;" name="class-type" value="${timetable.class_type}">
                <input style="display:none;" name="day" value="${timetable.day}">

                <button class="delete-course" type="submit">
                    <i class='bx bx-trash'></i>
                </button>
            </form>
        </div>
        <h2>${timetable.course_id}</h2>
        <p style="font-size:1vw;">${timetable.class_type}</p>`
        newDiv.style.gridRow = `${dayMap[day]}`;
        newDiv.style.gridColumn = `${timeMap[startTime]} / ${finalEndSpan}`;
        DivContainer.appendChild(newDiv);
    });
}

addCourseBtn.addEventListener('click', () => {
    heroSection.classList.toggle("hide-feature")
    courseForm.classList.toggle("hide")
})

closeForm.addEventListener('click', () => {
    heroSection.classList.toggle("hide-feature")
    courseForm.classList.toggle("hide")
})

editBtn.addEventListener('click', () => {
    listCourseDel.forEach(course => {
        course.classList.toggle("hide")
    });
})

document.addEventListener('DOMContentLoaded', function() {
    // List of available time options
    const timeOptions = [
        "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM", "6:00 PM"
    ];

    // Function to convert time string (e.g., "1:00 PM") into an hour and minute object
    function parseTime(timeStr) {
        let [hourMinute, period] = timeStr.split(' ');
        let [hour, minute] = hourMinute.split(':').map(num => parseInt(num, 10));
        if (period === "PM" && hour !== 12) {
            hour += 12; // Convert PM hours to 24-hour format
        }
        if (period === "AM" && hour === 12) {
            hour = 0; // Midnight is 00:00
        }
        return { hour, minute };
    }

    // Function to update the end-time options based on the selected start-time
    function updateEndTimeOptions(startTimeSelect, endTimeSelect) {
        const selectedStartTime = startTimeSelect.value;
        const startTimeObj = parseTime(selectedStartTime);

        // Clear existing options in the end-time select
        endTimeSelect.innerHTML = '';

        // Add a placeholder "Select" option
        let option = document.createElement('option');
        option.textContent = "—————SELECT—————";
        endTimeSelect.appendChild(option);

        // Add valid end-time options (only those that are after the selected start time)
        timeOptions.forEach(time => {
            const timeObj = parseTime(time);
            // Only add times that are after the selected start time
            if (timeObj.hour > startTimeObj.hour || (timeObj.hour === startTimeObj.hour && timeObj.minute > startTimeObj.minute)) {
                option = document.createElement('option');
                option.value = time;
                option.textContent = time;
                endTimeSelect.appendChild(option);
            }
        });
    }

    // Event listener for newly added .start-time elements (for dynamically added content)
    function handleStartTimeChange(event) {
        const startTimeSelect = event.target;
        const endTimeSelect = startTimeSelect.closest('div').querySelector('.end-time');
        updateEndTimeOptions(startTimeSelect, endTimeSelect);
    }

    // Event delegation for handling changes in dynamically added start-time elements
    document.body.addEventListener('change', function(event) {
        if (event.target.classList.contains('start-time')) {
            handleStartTimeChange(event);
        }
    });

    // Initialize all existing .start-time and .end-time pairs when the page loads
    const startTimeElements = document.querySelectorAll('.start-time');
    startTimeElements.forEach(startTimeSelect => {
        const endTimeSelect = startTimeSelect.closest('div').querySelector('.end-time');
        updateEndTimeOptions(startTimeSelect, endTimeSelect);
    });
});

editBtn.addEventListener('click', () => {
    deleteCourseFormAll = document.querySelectorAll(".delete-course-form")
    deleteCourseFormAll.forEach(ele => {
        ele.classList.toggle('hide')
    });
})