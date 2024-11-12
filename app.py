from flask import Flask, render_template, request, redirect, session, jsonify, json
from flask_mail import Mail, Message
import sqlite3
from datetime import datetime
from random import randint
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def create_connect_db(): 
    User_login_db = sqlite3.connect("Databases/System/User_data.db")
    User_db_cursor = User_login_db.cursor()
    User_db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        U_id INTEGER NOT NULL,
        email TEXT PRIMARY KEY,
        password INTEGER NOT NULL,
        date DATE NOT NULL
    )
''')
    
    try:
        User_db_cursor.execute('''INSERT INTO users (U_id, email, password, date) VALUES (1001, "abhas@example.com", 987654321, "2024-10-31")''')
    except:
        pass
    User_login_db.commit()
    User_login_db.close()

create_connect_db()

def create_User(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                        Course_id TEXT PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Credits TEXT NOT NULL,
                        Details TEXT,
                        Website TEXT,
                        Instructor_Name TEXT,
                        Instructor_Email TEXT )''')
    
    User_cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                        Course_id TEXT PRIMARY KEY,
                        Present INT NOT NULL,
                        Absent INT NOT NULL,
                        medical_leave INT NOT NULL)''')
    
    User_cursor.execute('''CREATE TABLE IF NOT EXISTS timetable (
                    monday TEXT ,
                    tuesday TEXT ,
                    wednesday TEXT ,
                    thursday TEXT ,
                    friday TEXT)''')
    
    User_cursor.execute('''INSERT INTO timetable (monday, tuesday, wednesday, thursday, friday) VALUES(" ", " ", " ", " ", " ")''')
    
    User_db.commit()
    User_db.close()

def if_table_exist(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    table_name = 'temp_attendance'

    User_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")

    table_exists = User_cursor.fetchone()
    User_db.close()

    if table_exists:
        return False
    else:
        return True

def create_temp_attendance(U_id, fin_timetable_list):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''CREATE TABLE IF NOT EXISTS temp_attendance (
                    course_id TEXT ,
                    class_type TEXT,
                    day TEXT,
                    start_time TEXT,
                    end_time TEXT )''')

    for i in fin_timetable_list:
        User_cursor.execute('''INSERT INTO temp_attendance (course_id, class_type, day, start_time, end_time) VALUES(?, ?, ?, ?, ?)''', (i['course_id'], i['class_type'], i['day'], i['start_time'],i['end_time']))
        User_db.commit()

    User_db.close()

    ans = read_temp_attendance(U_id)
    return ans

def read_temp_attendance(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()    

    User_cursor.execute('''SELECT * FROM temp_attendance''')
    read_data = User_cursor.fetchall()
    ans = []
    for i in read_data:
        temp_dict={}
        temp_dict['course_id'] = i[0]
        temp_dict['class_type'] = i[1]
        temp_dict['day'] = i[2]
        temp_dict['start_time'] = i[3]
        temp_dict['end_time'] = i[4]
        ans.append(temp_dict)

    User_db.close()
    print(ans)
    return ans

def remove_temp_attendance(U_id, Course_id, class_type):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute("DELETE FROM temp_attendance WHERE Course_id = ? AND class_type = ?", (Course_id, class_type))
    User_db.commit()
    
    if len(read_temp_attendance(U_id)) == 0:
        User_cursor.execute('''DROP TABLE temp_attendance''')
        User_db.commit()
        User_db.close()
        ans = ["Marked"]
    else:
        ans = read_temp_attendance(U_id)

    return ans

def give_day_code():
    today = datetime.today()
    day_name = today.strftime("%A")

    if day_name == "Monday":
        fin_day_name = "MON"
    elif day_name == "Tuesday":
        fin_day_name = "TUE"
    elif day_name == "Wednesday":
        fin_day_name = "WED"
    elif day_name == "Thursday":
        fin_day_name = "THUR"
    elif day_name == "Friday":
        fin_day_name = "FRI"
    elif day_name == "Saturday":
        fin_day_name = "SAT"
    elif day_name == "Sunday":
        fin_day_name = "SUN"

    return fin_day_name

def read_User_table():
    User_login_db = sqlite3.connect("Databases/System/User_data.db")
    User_db_cursor = User_login_db.cursor()

    User_db_cursor.execute("SELECT * from users")
    read_data = User_db_cursor.fetchall()
    User_login_db.close()
    return read_data

def auth_user(input_id, password):
    all_User_data = read_User_table()
    Ans = False
    for i in all_User_data:
        if str(i[0]) == input_id and str(i[2]) == str(password):
            Ans = True
            break
    return Ans

def write_User_table(U_id, email, password, date):
    User_login_db = sqlite3.connect("Databases/System/User_data.db")
    User_db_cursor = User_login_db.cursor()

    try:
        User_db_cursor.execute('''INSERT INTO users (U_id, email, password, date) Values (?, ?, ?, ?)''', (U_id, email, password, date))
        User_login_db.commit()
        User_login_db.close()
        return True
    except:
        return False
    
def write_User(U_id, course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    try:
        User_cursor.execute('''INSERT INTO courses (Course_id, Name, Credits, Details, Website, Instructor_Name, Instructor_Email) Values (?, ?, ?, ?, ?, ?, ?)''', (course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email))
        User_cursor.execute('''INSERT INTO attendance (Course_id, Present, Absent, medical_leave) Values (?, ?, ?, ?)''', (course_id, 0, 0, 0))
        User_db.commit()
        User_db.close()
        return True
    except:
        return False  

def read_User(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * from courses''')
    read_data = User_cursor.fetchall()
    User_db.close()
    return read_data  

def read_timetable(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * from timetable''')
    read_data = User_cursor.fetchall()
    User_db.close()
    try:
        read_data[0] = tuple(item.replace("'", '"') for item in read_data[0])
        data_list = [json.loads(item) for item in read_data[0]]
    except:
        data_list = [[],[],[],[],[]]
    return data_list

def write_timetable(U_id, timetable_list):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    prev_Data = read_timetable(U_id)

    User_cursor.execute('''DELETE FROM timetable''')
    
    mon, tue, wed, thur, fri = [], [], [], [], []

    for i in range(0, len(prev_Data)):
        if i == 0:
            mon+=prev_Data[i]
        elif i == 1:
            tue+=prev_Data[i]
        elif i== 2:
            wed+=prev_Data[i]
        elif i==3:
            thur+=prev_Data[i]
        elif i==4:
            fri+=prev_Data[i]

    for i in timetable_list:
        if i['day'] == "MON":
           mon+=[i]
        elif i['day'] == "TUE":
            tue+=[i]
        elif i['day'] == "WED":
            wed+=[i]
        elif i['day'] == "THUR":
            thur+=[i]
        elif i['day'] == "FRI":
            fri+=[i]

    User_cursor.execute('''INSERT INTO timetable 
                        (monday, tuesday, wednesday, thursday, friday) 
                        VALUES(?, ?, ?, ?, ?)''', (f"{mon}", f"{tue}", f"{wed}", f"{thur}", f"{fri}"))
    
    User_db.commit()
    User_db.close()
    
def del_User(U_id, C_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''DELETE FROM courses 
                        WHERE Course_id = ?''',(C_id,))
    User_cursor.execute('''DELETE FROM attendance 
                        WHERE Course_id = ?''',(C_id,))
    
    User_db.commit()
    User_db.close()

def read_User_attendance(U_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    User_cursor.execute('''SELECT * from attendance''')
    read_data = User_cursor.fetchall()
    User_db.close()
    return read_data

def write_User_attendance(U_id, attendance, Course_id):
    User_db = sqlite3.connect(f"Databases/Users/{U_id}_data.db")
    User_cursor = User_db.cursor()

    # Using placeholders for Course_id and dynamic column name substitution
    query = f"UPDATE attendance SET {attendance} = {attendance} + 1 WHERE Course_id = ?"
    User_cursor.execute(query, (Course_id,))

    User_db.commit()
    User_db.close()

def create_U_id():
    existing_U_id = []
    for i in read_User_table():
        existing_U_id.append(i[0])
    
    gen_U_id = existing_U_id[0]
    while gen_U_id in existing_U_id:
        gen_U_id = randint(1000, 9999)
    
    return gen_U_id

def generate_otp():
    return str(randint(100000, 999999))


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/')
def home():
    return redirect('Sign-In')

@app.route("/Home", methods=['GET', 'POST'])
def main_Web():
    attendance = read_User_attendance(session['U_id'])
    return render_template('index.html', attendance = attendance)

@app.route("/Sign-In", methods=['GET', 'POST'])
def Sign_In_Web():
    if request.method == 'POST':
        input_id = request.form["signin-i'd"]
        password = request.form['signin-password']
        if auth_user(input_id, password):
            session.clear()
            session['U_id'] = input_id
            return redirect('Home')
        else:
            return "error! Invalid Credentials"

    return render_template('Signin.html')

@app.route("/Sign-Up", methods=['GET', 'POST'])
def Sign_Up_Web():
    if request.method == 'POST':
        email = request.form['signup-email']
        password = request.form['signup-password']
        session.clear()

        session['email'] = email
        session['password'] = password
        session.pop('OTP', None)
        return redirect("/Verify-OTP")
        
    return render_template('Signup.html')

@app.route("/Verify-OTP", methods=['GET', 'POST'])
def Verify_User():
    U_id = create_U_id()
    email = session.get('email')
    password = session.get('password')
    date = datetime.today().date()
    if 'OTP' not in session:
        OTP = generate_otp()
        
        session['OTP'] = OTP

        html_content = render_template("email_template.html", email=email, OTP=OTP)
        msg_sender = os.getenv('MAIL_USERNAME')
        msg = Message("Please verify your email", sender=msg_sender, recipients=[email])
        msg.html = html_content

        try:
            mail.send(msg)
        except Exception as e:
            return f'Failed to send OTP: {e}'

    if request.method == 'POST':
        entered_OTP = request.form['entered_OTP']

        OTP = session.get('OTP')
        
        if entered_OTP == OTP:
            if write_User_table(U_id, email, password, date):
                msg_sender = os.getenv('MAIL_USERNAME')
                new_msg = Message('Account Created', sender=msg_sender, recipients=[email])
                new_msg.body = f"This is a system generated Mail. Please Do not reply. \nYour Login Credentials \nKeep Your Credentials safe and avoid sharing with others. \nUser I'd: {U_id}\nPassword: {password} \nThank you for chosing us ❤️."
                session.pop('OTP', None)
                create_User(U_id)
            
                try:
                    mail.send(new_msg)
                except Exception as e:
                    return f'Failed to send OTP: {e}'
                
                session.pop('email', None)
                session.pop('password', None)

                session['U_id'] = U_id
                
                return redirect('Home')
            else:
                return "Error! Email already used..."
        else:
            return "OTP does not match!!!"
    
    return render_template('Signup-OTP.html', email=email)

@app.route("/Add-Course", methods = ['GET', 'POST'])
def Add_Course():
    courses = read_User(session['U_id'])
    form_name = request.form.get('form-name')

    if request.method == 'POST' and form_name == "add-course":
        course_id = request.form.get('form-course-id')
        course_name = request.form.get('form-course-name')
        course_credits = request.form.get('form-course-credits')
        course_details = request.form.get('form-course-details')
        course_website = request.form.get('form-course-website')
        Instructor_name = request.form.get('form-instructor')
        Instructor_email = request.form.get('form-instructor-email')

        if write_User(session['U_id'], course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email):
            print("success")
            return redirect("Add-Course")
        else:
            return "Error. Course already exists."
        
    if request.method == 'POST' and form_name == "delete-course":
        C_id = request.form.get("C_id")
        del_User(session['U_id'], C_id)
        courses = read_User(session['U_id'])

    return render_template('AddCourse.html', courses = courses)

@app.route("/Mark-Attendance", methods = ['GET', 'POST'])
def Mark_Attendance():
    timetables = read_timetable(session['U_id'])
    timetables_list = [item for sublist in timetables for item in sublist]
    courses = read_User(session['U_id'])
    fin_day_name=give_day_code()

    fin_timetables_list_test=[]
    for i in timetables_list:
        if i['day'] == fin_day_name:
            fin_timetables_list_test.append(i)
    
    if if_table_exist(session['U_id']):
        fin_timetables_list = create_temp_attendance(session['U_id'], fin_timetables_list_test)
    else:
        fin_timetables_list = read_temp_attendance(session['U_id'])

    if request.method == 'POST':
        course_id = request.form.get("form-course-id")
        class_type = request.form.get("form-class-type")
        attendance = request.form.get("attendance")

        fin_timetables_list = remove_temp_attendance(session['U_id'], course_id, class_type)
        
        write_User_attendance(session['U_id'], attendance, course_id)
        

    return render_template('MarkAttendance.html', courses=courses, fin_timetables_list=fin_timetables_list, fin_day_name=fin_day_name)

@app.route("/Today-Schedule", methods = ['GET', 'POST'])
def Schedule():
    timetables = read_timetable(session['U_id'])
    timetables_list = [item for sublist in timetables for item in sublist]
    courses = read_User(session['U_id'])
    form_name = request.form.get('form-name')

    if request.method == 'POST' and form_name == "add-course":
        form_data = request.form

        all_forms_data = []

        for key, value in form_data.items():
        # Extract the form index (e.g., from form-course-name-123, we extract 123)
            if key.startswith('course-id-'):
                form_index = key.split('-')[-1]
                # Now create a dictionary for this form's data
                form_dict = {
                    'course_id': form_data.get(f'course-id-{form_index}'),
                    'class_type': form_data.get(f'class-type-{form_index}'),
                    'day': form_data.get(f'day-{form_index}'),
                    'start_time': form_data.get(f'class-start-time-{form_index}'),
                    'end_time': form_data.get(f'class-end-time-{form_index}')
                }
                all_forms_data.append(form_dict)

        write_timetable(session['U_id'], all_forms_data)
        timetables = read_timetable(session['U_id'])
        timetables_list = [item for sublist in timetables for item in sublist]
        courses = read_User(session['U_id'])
        
    if request.method == 'POST' and form_name == "delete-course":
        C_id = request.form.get("C_id")
        del_User(session['U_id'], C_id)
        timetables = read_timetable(session['U_id'])
        timetables_list = [item for sublist in timetables for item in sublist]
        courses = read_User(session['U_id'])

    return render_template('Schedule.html', timetables_list=timetables_list, courses=courses)

@app.route("/Analytics", methods = ['GET', 'POST'])
def Course_Analytics():
    attendance = read_User_attendance(session['U_id'])
    return render_template('Analytics-web.html', attendance=attendance)

@app.route("/Grades", methods = ['GET', 'POST'])
def Grades():
    return render_template('Grades.html')

@app.route("/Log-Out", methods = ['GET', 'POST'])
def Logout():
    session.clear()
    return redirect("Sign-In")

if __name__ == "__main__":
    app.run(debug=True, port=8000)