Attendance Management Website
This is a web-based Attendance Management System created as a college project using Python, Flask, HTML, CSS, JavaScript, and SQLite. It provides a streamlined way for users to sign up, sign in, and manage attendance for selected courses.

Features
User Authentication: Secure sign-up and sign-in system with email OTP verification.
Course Selection: Allows users to select courses for attendance tracking.
Dynamic Course List: Courses that have already been submitted in the attendance form no longer appear in the list, even after a page reload.
Database Management: Each new user is assigned a unique database with relevant tables for their attendance records, stored persistently using SQLite3.
Responsive Design: Works smoothly across devices, ensuring accessibility and ease of use.
Project Structure
Frontend: Built with HTML, CSS, and JavaScript for a clean and responsive UI.
Backend: Built with Python and Flask for server-side processing, handling authentication and database interactions.
Database: Utilizes SQLite3 to store and manage user data and attendance records, ensuring data persistence across sessions.
Usage
Sign Up: Users can register by providing an email and password. After registration, an OTP is sent to verify the email.
Sign In: Redirects users to the sign-in page for access to the dashboard.
Manage Attendance: Users can add and track their attendance for selected courses.
Deployment
The application is designed for easy deployment on platforms like Render, Railway, DigitalOcean, or Vercel, which support Flask applications with SQLite database persistence.

Technologies Used
Python
Flask
HTML5
CSS3
JavaScript
SQLite3