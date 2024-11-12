toggle = document.querySelector(".toggle");
sidebar = document.querySelector(".side-bar");
logout = document.querySelector(".nav-link-1");
courseAnalytics = document.querySelector(".course-analytics")
listSbOptions = document.querySelectorAll(".nav-link a")

async function fetchAtData() {
    try {
        attendanceDataEle = document.querySelector("#attendance").textContent;

        attendanceData = JSON.parse(attendanceDataEle);

        if (attendanceData.length != 0) {
            let num=0
            attendanceData.forEach(course => {
                num++
                wrapperDiv = document.createElement('div');
                wrapperDiv.classList.add('wrapper-div');
                wrapperDiv.setAttribute('id', `course-${num}`)
                newCourseDiv = document.createElement('div');
                newCourseDiv.classList.add(`course-${num}`, 'course');
                wrapperDiv.appendChild(newCourseDiv)
                calcDiv = document.createElement('div')
                calcDiv.classList.add('calc-div')
                calcDiv.innerHTML += `
                <h2>Attenance</h2>
                <div class='show-attendance'>
                    <div class='present display-attendance'>
                        <p>Present</p>
                        <h1>${course[1]}</h1>
                    </div>
                    <div class='absent display-attendance'>
                        <p>Absent</p>
                        <h1>${course[2]}</h1>
                    </div>
                    <div class='mleave display-attendance'>
                        <p>Medical leave</p>
                        <h1>${course[3]}</h1>
                    </div>
                </div>
                <div class='calc-buttons'>
                    <button class='${course[0].replaceAll(" ", "_")} btns presence-btn'>Presence %</button>
                    <button class='btns leave-btn'>Leave calculator</button>
                </div>
                `
                wrapperDiv.appendChild(calcDiv);
                courseAnalytics.appendChild(wrapperDiv);

                if (course[1] == 0 && course[2] == 0 && course[3] ==0){
                    newHead = document.createElement('h2');
                    newpara = document.createElement('p');
                    newHead.textContent = `${course[0]}`
                    newpara.textContent = "No Data to display."
                    newHead.classList.add('analytics-div-head');
                    newpara.classList.add('analytics-div-para');
                    newCourseDiv.appendChild(newHead);
                    newCourseDiv.appendChild(newpara);
                } else{
                    let pie = new ej.charts.AccumulationChart({
                        series: [
                            {
                    
                                dataSource: [
                                    { x: 'Present', y: course[1], r: '92.5' },
                                    { x: 'Absent', y: course[2], r: '92.5' },
                                    { x: 'Medical leave', y: course[3], r: '92.5' },
                                ],
                                dataLabel: {
                                    visible: false, position: 'none',
                                    name: 'x'
                    
                                },
                                radius: 'r', xName: 'x',
                                yName: 'y', innerRadius: '20%'
                            },
                    
                        ],
                        enableSmartLabels: false,
                        legendSettings: {
                            visible: true,
                        },
                        enableAnimation: true,
                        title: `${course[0]} Attendance`
                    }, '#element');
                    
                    pie.appendTo(newCourseDiv);
                }
            });
        } else{
            alertDiv = document.createElement('div')
            alertDiv.classList.add('alert-div')
            alertDiv.innerHTML += `
            <h1>No Courses To Display. </h1>
            <a href="Add-Course" class="sub-alert-div">
                <i class='bx bx-book-add'></i>
                <p>Add course</p>
            </a>`
            courseAnalytics.appendChild(alertDiv);
        }

    } catch (error) {
        console.error("Error parsing attendance data:", error);
    }
};

currPage = window.location.pathname;
listSbOptions[4].classList.add("is-active")
fetchAtData()


toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close")
    logout.classList.toggle("close")
    toggle.classList.toggle("close")
})

presenceCalc = document.querySelectorAll(".presence-btn");

console.log(attendanceData);

presenceCalc.forEach(btn => {
    btn.addEventListener('click', () => {
        reqList=Array.from(btn.classList)
        course = reqList[0].replaceAll("_", " ")
        for (i = 0; i < attendanceData.length; i++) {
            if (attendanceData[i][0] == course) {
                sum = attendanceData[i][1]+attendanceData[i][2]+attendanceData[i][3]
                if (sum != 0) {
                    ans = (attendanceData[i][1]*100)/sum
                }else{
                    ans = 0
                }
                break
            }
        }
        alert(`Attendance % in ${course} is ${ans}`)
    })
});