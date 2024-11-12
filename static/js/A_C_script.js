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

editBtn.addEventListener('click', () => {
    listCourseDel.forEach(course => {
        course.classList.toggle("hide")
    });
})