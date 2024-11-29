from flask import Flask, render_template, request, redirect, session, url_for, json, send_from_directory
from flask_mail import Mail, Message
from datetime import datetime, timedelta, time, timezone
from random import randint
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from urllib.parse import urlparse
import pg8000
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

database_url = os.getenv("DATABASE_URL")
result = urlparse(database_url)

connection = pg8000.connect(
    user=result.username,
    password=result.password,
    host=result.hostname,
    port=5432,
    database=result.path[1:]
)

def create_connect_db(): 
    connection_cursor = connection.cursor()
    connection_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            U_id INTEGER NOT NULL,
                            email TEXT PRIMARY KEY,
                            password TEXT NOT NULL,
                            date DATE NOT NULL,
                            login_U_id TEXT NOT NULL
                            )
                            ''')
    connection_cursor.execute('''INSERT INTO users 
                            (U_id, email, password, date, login_U_id)
                            VALUES (1001, 'abc@example.com', 987654321, '2024-10-15', '2024abhas1001')
                            ON CONFLICT (email) DO NOTHING;''')
    
    connection_cursor.execute('''CREATE TABLE IF NOT EXISTS deleted_users (
                            U_id INTEGER NOT NULL,
                            email TEXT,
                            password TEXT NOT NULL,
                            date DATE NOT NULL,
                            deleting_date DATE NOT NULL
                            )
                            ''')
    
    connection_cursor.execute('''CREATE TABLE IF NOT EXISTS grades_users (
                        U_id INTEGER NOT NULL,
                        sgpa TEXT,
                        permission TEXT NOT NULL
                        )
                        ''')

    connection.commit()

def give_day_code(day_name):

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

def update_deleted_users(U_id, email, password, date):
    connection_cursor = connection.cursor()
    deleting_date =datetime.today().date()
    connection_cursor.execute(f'''INSERT INTO deleted_users 
                            (U_id, email, password, date, deleting_date) 
                            VALUES (%s, %s, %s, %s, %s);''', (U_id, email, password, date, deleting_date))

    connection.commit()

def read_User_table():
    connection_cursor = connection.cursor()

    connection_cursor.execute("SELECT * from users")
    read_data = connection_cursor.fetchall()
    return read_data

def read_grades_table():
    connection_cursor = connection.cursor()

    connection_cursor.execute("SELECT * from grades_users")
    read_data = connection_cursor.fetchall()
    return read_data

def drop_table(U_id, date):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''DROP TABLE IF EXISTS "{U_id}_{date.strftime("%Y-%m-%d").replace("-", "_")}"''')

    connection.commit()

def update_day_tracker(U_id):
    User_cursor = connection.cursor()
    date = datetime.today().date()
    day = give_day_code(date.strftime("%A"))
    yesterday_date = date - timedelta(days = 1)
    yesterday_day = give_day_code(yesterday_date.strftime('%A'))

    try:
        User_cursor.execute(f'''INSERT INTO "{U_id}_day_tracker" (day, date, attendance) VALUES (%s, %s, %s)''', (day, date, "UNMARKED"))
        User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_{date.strftime("%Y-%m-%d").replace("-", "_")}" (
                    course_id TEXT,
                    class_type TEXT ,
                    day TEXT ,
                    start_time TEXT ,
                    end_time TEXT)''')
        drop_table(U_id, yesterday_date)

        connection.commit()
        all_courses_of_the_day = read_day(U_id, yesterday_day)
        
        for i in all_courses_of_the_day:
            write_User_attendance(U_id, "Absent", i[0], i[1])
            connection.commit()
        
    except:
        connection.rollback()
    
    connection.commit()

def create_User(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_courses" (
                        Course_id TEXT PRIMARY KEY,
                        Name TEXT NOT NULL,
                        Credits TEXT NOT NULL,
                        Details TEXT,
                        Website TEXT,
                        Instructor_Name TEXT,
                        Instructor_Email TEXT )''')
    connection.commit()

    User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_attendance" (
                        Course_id TEXT PRIMARY KEY,
                        Present JSONB NOT NULL,
                        Absent JSONB NOT NULL,
                        medical_leave JSONB NOT NULL)''')
    connection.commit()

    User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_grades" (
                        Course_id TEXT PRIMARY KEY,
                        grades_overview JSONB NOT NULL,
                        user_grades JSONB NOT NULL)''')
    connection.commit()

    User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_timetable" (
                    monday TEXT ,
                    tuesday TEXT ,
                    wednesday TEXT ,
                    thursday TEXT ,
                    friday TEXT)''')
    connection.commit()

    User_cursor.execute(f'''INSERT INTO "{U_id}_timetable" 
                        (monday, tuesday, wednesday, thursday, friday) 
                        VALUES('[]', '[]', '[]', '[]', '[]')''')
    connection.commit()

    User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_userDetails" (
                    U_id TEXT PRIMARY KEY,
                    user_name TEXT ,
                    user_email TEXT ,
                    joined_date TEXT ,
                    profile_image_url TEXT, 
                    courses_registered INT)''')
    connection.commit()

    days_list = ['MON', 'TUE', 'WED', 'THUR', 'FRI', 'SAT', 'SUN']

    for i in days_list:
        User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_{i}" (
                course_id TEXT,
                class_type TEXT ,
                day TEXT ,
                start_time TEXT ,
                end_time TEXT)''')
        connection.commit()

    User_cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{U_id}_day_tracker" (
                        day TEXT,
                        date TEXT PRIMARY KEY,
                        attendance TEXT)''')
    connection.commit()
    
    update_day_tracker(U_id)

    insert_details = read_User_table()
    for i in insert_details:
        if i[0] == U_id:
            user_email = i[1]
            joined_date = i[3]

    User_cursor.execute(f'''INSERT INTO "{U_id}_userDetails" 
                        (U_id, user_name, user_email, joined_date, profile_image_url, courses_registered) 
                        VALUES(%s, '', %s, %s, '', 0)''', (U_id, user_email, joined_date))

    connection.commit()

def reset_User(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''UPDATE grades_users
                        SET sgpa = 0
                        WHERE U_id = %s''', (U_id,))
    connection.commit()

    User_cursor.execute(f'''UPDATE "{U_id}_Userdetails"
                        SET courses_registered = 0
                        WHERE U_id = %s''', (U_id,))
    connection.commit()

    User_cursor.execute(f'''DELETE FROM "{U_id}_courses"''')
    connection.commit()

    User_cursor.execute(f'''DELETE FROM "{U_id}_attendance"''')
    connection.commit()

    User_cursor.execute(f'''DELETE FROM "{U_id}_grades"''')
    connection.commit()

    User_cursor.execute(f'''DELETE FROM "{U_id}_timetable"''')
    connection.commit()

    User_cursor.execute(f'''INSERT INTO "{U_id}_timetable" 
                        (monday, tuesday, wednesday, thursday, friday) 
                        VALUES('[]', '[]', '[]', '[]', '[]')''')
    connection.commit()

    days_list = ['MON', 'TUE', 'WED', 'THUR', 'FRI', 'SAT', 'SUN']

    for i in days_list:
        User_cursor.execute(f'''DELETE FROM "{U_id}_{i}"''')
        connection.commit()

    User_cursor.execute(f'''DELETE FROM "{U_id}_day_tracker"''')
    connection.commit()
    
    update_day_tracker(U_id)

    connection.commit()

def read_date_table(U_id):
    date = datetime.today().date()
    User_cursor = connection.cursor()

    try:
        User_cursor.execute(f'''SELECT * FROM "{U_id}_{date.strftime("%Y-%m-%d").replace("-", "_")}" ''')  
        read_data = User_cursor.fetchall()
    except :
        connection.rollback()
        read_data = []

    return read_data  

def mark_table(U_id):
    date = datetime.today().date()
    User_cursor = connection.cursor()

    User_cursor.execute(f'''UPDATE "{U_id}_day_tracker"
                        SET attendance = 'MARKED'
                        WHERE date = %s''', (date,))
    connection.commit()

def check_today_attendance(U_id):
    date = datetime.today().date()
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * FROM "{U_id}_day_tracker"''')

    read_data = User_cursor.fetchall()

    connection.commit() 

    for i in read_data:
        if i[1] == str(date):
            ans = i 
     
    return ans

def check_attendance(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * FROM "{U_id}_day_tracker"''')

    read_data = User_cursor.fetchall()

    connection.commit() 

    return read_data

def write_date_table(U_id, data):
    date = datetime.today().date()
    User_cursor = connection.cursor()

    User_cursor.execute(f'''INSERT INTO "{U_id}_{date.strftime("%Y-%m-%d").replace("-", "_")}" 
                        (course_id, class_type, day, start_time, end_time) 
                        VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}')''')

    connection.commit()

def read_userDetails(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * FROM "{U_id}_userDetails"''')
    read_data = User_cursor.fetchall()

    return read_data

def update_userDetails(U_id, user_name, profile_image_url):
    User_cursor = connection.cursor()

    if user_name != "":
        User_cursor.execute(f'''UPDATE "{U_id}_userDetails" 
            SET user_name = %s 
            WHERE U_id = %s''', 
            (user_name, U_id)) 

    User_cursor.execute(f'''UPDATE "{U_id}_userDetails" 
                    SET profile_image_url = %s 
                    WHERE U_id = %s''', 
                    (profile_image_url, U_id)) 
    
    connection.commit() 

def read_day(U_id, day):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * from "{U_id}_{day}"''')

    read_data = User_cursor.fetchall()

    return read_data


def update_course_number(U_id):
    User_cursor = connection.cursor()
    
    query = f'UPDATE "{U_id}_userDetails" SET courses_registered = courses_registered + 1 WHERE U_id = %s'
    User_cursor.execute(query, (U_id,))

    connection.commit()

def read_courses(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * FROM "{U_id}_courses"''') 
    read_data = User_cursor.fetchall()
    ans = 0
    for i in read_data:
        ans+=1
    return ans

def auth_user(input_id, password):
    all_User_data = read_User_table()
    Ans = False
    for i in all_User_data:
        if str(i[4]) == input_id and str(i[2]) == str(password):
            Ans = True
            break
    return Ans

def write_User_table(U_id, email, password, date, login_U_id):
    connection_cursor = connection.cursor()
    try:
        connection_cursor.execute(f'''INSERT INTO users 
                                  (U_id, email, password, date, login_U_id) 
                                  Values (%s, %s, %s, %s, %s)''', 
                                  (U_id, email, password, date, login_U_id))
        
        connection_cursor.execute(f'''INSERT INTO grades_users 
                                  (U_id, sgpa, permission) 
                                  Values (%s, %s, %s)''', 
                                  (U_id, 0, "NO"))

        connection.commit()
        return True
    except:
        connection.rollback()
        return False
    
def delete_User_table(U_id):
    connection_cursor = connection.cursor()

    connection_cursor.execute(f'''DELETE FROM users
                                WHERE U_id = %s ''', (U_id,))
    

    connection_cursor.execute(f'''DELETE FROM grades_users
                                WHERE U_id = %s ''', (U_id,))
    
    connection.commit()

    
def write_User(U_id, course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email):
    User_cursor = connection.cursor()

    try:
        User_cursor.execute(f'''INSERT INTO "{U_id}_courses"
                            (Course_id, Name, Credits, Details, Website, Instructor_Name, Instructor_Email) 
                            Values (%s, %s, %s, %s, %s, %s, %s)''', 
                            (course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email))

        default_data = {"LECTURE" : 0, "TUTORIAL" : 0, "LAB" : 0, "INTRODUCTION" : 0}

        User_cursor.execute(f'''INSERT INTO "{U_id}_attendance" 
                            (Course_id, Present, Absent, medical_leave) 
                            VALUES(%s, %s, %s, %s)''', 
                            (course_id, default_data, default_data, default_data))

        connection.commit()

        return True
    except:
        connection.rollback()
        return False  

def read_User(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * from "{U_id}_courses"''')
    read_data = User_cursor.fetchall()
    return read_data  

def read_timetable(U_id):
    User_cursor = connection.cursor()
    User_cursor.execute(f'''SELECT * FROM "{U_id}_timetable"''')
    read_data = User_cursor.fetchall()

    try:
        read_data_list = list(read_data[0])
        read_data_list = tuple(
            item.replace("'", '"') if item.strip() else "[]" for item in read_data[0]
        )
        data_list = [json.loads(item) for item in read_data_list]
    except json.JSONDecodeError:
        data_list = [[], [], [], [], []]

    return data_list

def delete_timetable(U_id, C_id, class_type, day):
    User_cursor = connection.cursor()
    prev_Data = read_timetable(U_id)

    User_cursor.execute(f'''DELETE FROM "{U_id}_timetable"''')
    
    mon, tue, wed, thur, fri = [], [], [], [], []
    list_days = [mon, tue, wed, thur, fri]
    list_days_name = ["MON", "TUE", "WED", "THUR", "FRI"]

    day_idx = list_days_name.index(day)

    for i in list_days_name:
        User_cursor.execute(f'''DELETE FROM "{U_id}_{i}"''')

    for i in range(0, len(prev_Data)):
        if i == 0:
            if day_idx == i:
                prev_Data[i] = [d for d in prev_Data[i] if d["course_id"] != C_id and d["class_type"] != class_type]
            mon+=prev_Data[i]
        elif i == 1:
            if day_idx == i:
                prev_Data[i] = [d for d in prev_Data[i] if d["course_id"] != C_id and d["class_type"] != class_type]
            tue+=prev_Data[i]
        elif i== 2:
            if day_idx == i:
                prev_Data[i] = [d for d in prev_Data[i] if d["course_id"] != C_id and d["class_type"] != class_type]
            wed+=prev_Data[i]
        elif i==3:
            if day_idx == i:
                prev_Data[i] = [d for d in prev_Data[i] if d["course_id"] != C_id and d["class_type"] != class_type]
            thur+=prev_Data[i]
        elif i==4:
            if day_idx == i:
                prev_Data[i] = [d for d in prev_Data[i] if d["course_id"] != C_id and d["class_type"] != class_type]
            fri+=prev_Data[i]

    User_cursor.execute(f'''INSERT INTO "{U_id}_timetable" 
                        (monday, tuesday, wednesday, thursday, friday) 
                        VALUES(%s, %s, %s, %s, %s)''', (f'{mon}', f'{tue}', f'{wed}', f'{thur}', f'{fri}'))
    idx=0
    for i in list_days:
        for j in i:
            User_cursor.execute(f'''INSERT INTO "{U_id}_{list_days_name[idx]}"
                                (course_id, class_type, day, start_time, end_time) 
                                VALUES(%s, %s, %s, %s, %s)''', (j['course_id'], j['class_type'], j['day'], j['start_time'], j['end_time']))
        idx+=1

    connection.commit()


def write_timetable(U_id, timetable_list):
    User_cursor = connection.cursor()

    prev_Data = read_timetable(U_id)

    User_cursor.execute(f'''DELETE FROM "{U_id}_timetable"''')
    
    mon, tue, wed, thur, fri = [], [], [], [], []
    list_days = [mon, tue, wed, thur, fri]
    list_days_name = ["MON", "TUE", "WED", "THUR", "FRI"]

    for i in list_days_name:
        User_cursor.execute(f'''DELETE FROM "{U_id}_{i}"''')

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

    User_cursor.execute(f'''INSERT INTO "{U_id}_timetable" 
                        (monday, tuesday, wednesday, thursday, friday) 
                        VALUES(%s, %s, %s, %s, %s)''', (f'{mon}', f'{tue}', f'{wed}', f'{thur}', f'{fri}'))
    idx=0
    for i in list_days:
        for j in i:
            User_cursor.execute(f'''INSERT INTO "{U_id}_{list_days_name[idx]}"
                                (course_id, class_type, day, start_time, end_time) 
                                VALUES(%s, %s, %s, %s, %s)''', (j['course_id'], j['class_type'], j['day'], j['start_time'], j['end_time']))
        idx+=1

    connection.commit()
    
def del_User(U_id, C_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''DELETE FROM "{U_id}_courses" 
                        WHERE Course_id = %s''',(C_id,))
    User_cursor.execute(f'''DELETE FROM "{U_id}_attendance" 
                        WHERE Course_id = %s''',(C_id,))
    
    connection.commit()

def read_User_attendance(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * from "{U_id}_attendance"''')
    read_data = User_cursor.fetchall()
    return read_data

def write_User_attendance(U_id, attendance, Course_id, class_type):
    req_data = read_User_attendance(U_id)
    User_cursor = connection.cursor()

    class_attendance_map = {"Present": 1, "Absent": 2, "medical_leave": 3}

    class_attendance_value = class_attendance_map[str(attendance)]

    for i in req_data:
        if str(i[0]) == str(Course_id):
            req_ans = i
            break

    req_attendance = req_ans[class_attendance_value]

    req_attendance[str(class_type)] += 1

    attendance = attendance.lower()
    req_attendance_json = json.dumps(req_attendance)

    User_cursor.execute(f'''
        UPDATE "{U_id}_attendance" 
        SET "{attendance}" = %s 
        WHERE Course_id = %s
    ''', (req_attendance_json, Course_id))

    connection.commit()

def read_User_grades(U_id):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''SELECT * from "{U_id}_grades"
                        ORDER BY Course_id ASC ''')
    read_data = User_cursor.fetchall()

    return read_data

def write_User_grades(U_id, Course_id, course_dict):
    User_cursor = connection.cursor()

    default_user_grades={}

    for keys in course_dict:
        default_user_grades[keys] = "-"

    course_dict_json = json.dumps(course_dict)
    default_user_grades_json = json.dumps(default_user_grades)
    try:
        User_cursor.execute(f'''INSERT INTO "{U_id}_grades" 
                            (Course_id, grades_overview, user_grades)
                            VALUES (%s, %s, %s)''', 
                            (Course_id, course_dict_json, default_user_grades_json))
        connection.commit()
    except:
        connection.rollback()

def update_user_grades(U_id, final_ans):
    User_cursor = connection.cursor()

    final_ans_json = json.dumps(final_ans[2])
    User_cursor.execute(f'''UPDATE "{U_id}_grades" 
                        SET user_grades = %s
                        WHERE Course_id = %s''', 
                        (final_ans_json, final_ans[0]))
    connection.commit()

def update_concent(U_id, concent_value):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''UPDATE grades_users 
                        SET permission = %s
                        WHERE U_id = %s''', 
                        (concent_value, U_id))
    connection.commit()

def update_user_grades_table(U_id, sgpa):
    User_cursor = connection.cursor()

    User_cursor.execute(f'''UPDATE grades_users 
                        SET sgpa = %s
                        WHERE U_id = %s''', 
                        (sgpa, U_id))
    connection.commit()

def give_grade_value(your_total, final_total):
    temp = (your_total / final_total) * 100
    if temp > 80 and temp < 100:
        return 10
    elif temp > 70 and temp < 80:
        return 9
    elif temp > 60 and temp < 70:
        return 8
    elif temp > 50 and temp < 60:
        return 7
    elif temp > 40 and temp < 50:
        return 6
    elif temp > 30 and temp < 40:
        return 5
    elif temp > 20 and temp < 30:
        return 4
    elif temp > 10 and temp < 20:
        return 2
    elif temp > 0 and temp < 10:
        return 0
    else:
        return 0

def calculate_sgpa(grades_data, courses_data):
    net_user_total = 0
    net_final_total = 0
    for data in grades_data:
        for course in courses_data:
            if str(data[0]) == str(course[0]):
                credits = int(course[2])

        your_total = 0
        final_total = 0
        for key,value in data[1].items():
            if data[2][key] != "-":
                your_total += float(data[2][key])
                final_total += float(data[1][key])

        if final_total == 0:
            expected_grade = 0
            credits = 0
        else:
            expected_grade = give_grade_value(your_total, final_total)
        net_user_total += expected_grade * credits
        net_final_total += credits

    final_sgpa = net_user_total / net_final_total
    fin_ans = round(final_sgpa, 2)
    return fin_ans

def create_U_id():
    existing_U_id = []
    for i in read_User_table():
        existing_U_id.append(i[0])
    
    gen_U_id = existing_U_id[0]
    while gen_U_id in existing_U_id:
        gen_U_id = randint(1000, 9999)
    
    return gen_U_id

def Gen_login_U_id(U_id, name, joining_year):
    name_list = name.split()
    ans = str(joining_year) + name_list[0].lower() + str(U_id)

    return ans

def generate_otp():
    return str(randint(100000, 999999))

app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/Update-Databases', methods=['GET', 'POST', 'HEAD'])
def update_databases():
    local_time = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    current_time = local_time.time()
    start_time = time(6, 15)
    end_time = time(6, 45)

    if start_time <= current_time <= end_time:
        existingUsers = read_User_table()
        for user in existingUsers:
            update_day_tracker(user[0])

        if request.method == 'HEAD':
            return "", 200 
        
        return "Successful"
    
    else:

        return "Unsuccessful"

@app.route('/', methods=['GET', 'POST', 'HEAD'])
def home():
    create_connect_db()
    if request.method == 'POST':
        reset_User(session['U_id'])
        return redirect('Home')

    return redirect('Sign-In')

@app.route("/Home", methods=['GET', 'POST', 'HEAD'])
def main_Web():
    read_data_user = read_userDetails(session['U_id'])
    attendance = read_User_attendance(session['U_id'])
    return render_template('index.html', attendance = attendance, read_data_user=read_data_user)

@app.route("/Sign-In", methods=['GET', 'POST', 'HEAD'])
def Sign_In_Web():
    if request.method == 'POST':
        input_id = request.form["signin-i'd"]
        password = request.form['signin-password']

        if auth_user(input_id, password):
            session.clear()
            session['U_id'] = input_id[-4:]
            return redirect('Home')
        else:
            connection.rollback()
            return "error! Invalid Credentials"

    return render_template('Signin.html')

@app.route("/Sign-Up", methods=['GET', 'POST', 'HEAD'])
def Sign_Up_Web():
    if request.method == 'POST':
        email = request.form['signup-email']
        password = request.form['signup-password']
        name = request.form['signup-name']
        joining_year = request.form['signup-year']
        session.clear()

        session['email'] = email
        session['password'] = password
        session['name'] = name
        session['joining_year'] = joining_year

        session.pop('OTP', None)
        return redirect("/Verify-OTP")
        
    return render_template('Signup.html')

@app.route("/Verify-OTP", methods=['GET', 'POST', 'HEAD'])
def Verify_User():
    email = session.get('email')
    password = session.get('password')
    name = session.get('name')
    joining_year = session.get('joining_year')

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
            U_id = create_U_id()
            login_U_id = Gen_login_U_id(U_id, name, joining_year)
            if write_User_table(U_id, email, password, date, login_U_id):
                msg_sender = os.getenv('MAIL_USERNAME')
                new_msg = Message('Account Created', sender=msg_sender, recipients=[email])
                new_msg.body = f"This is a system generated Mail. Please Do not reply. \nYour Login Credentials \nKeep Your Credentials safe and avoid sharing with others. \nUser I'd: {login_U_id}\nPassword: {password} \nThank you for chosing us ❤️."
                session.pop('OTP', None)
                create_User(U_id)
                name = name.title()
                update_userDetails(U_id, name, "")
            
                try:
                    mail.send(new_msg)
                except Exception as e:
                    return f'Failed to send OTP: {e}'
                
                session.pop('email', None)
                session.pop('password', None)
                session.pop('joining_year', None)

                session['U_id'] = U_id
                
                return redirect('Home')
            else:
                connection.rollback()
                return "Error! Email already used..."
        else:
            connection.rollback()
            return "OTP does not match!!!"
    
    return render_template('Signup-OTP.html', email=email)

@app.route("/Add-Course", methods=['GET', 'POST', 'HEAD'])
def Add_Course():
    read_data_user = read_userDetails(session['U_id'])
    courses = read_User(session['U_id'])
    form_name = request.form.get('form-name')

    if request.method == 'POST' and form_name == "add-course":
        course_id = request.form.get('form-course-id')
        check = course_id.split(" ")
        if len(check) > 1:
            course_name_id = check[0]
            course_level = check[1]
            course_id = course_name_id.upper()+" "+course_level
        else:
            course_name_id = course_id[0:3]
            course_level = course_id[3:6]
            course_id = course_name_id.upper()+" "+course_level

        course_name = request.form.get('form-course-name')
        course_credits = request.form.get('form-course-credits')
        course_details = request.form.get('form-course-details')
        course_website = request.form.get('form-course-website')
        Instructor_name = request.form.get('form-instructor')
        Instructor_email = request.form.get('form-instructor-email')

        if write_User(session['U_id'], course_id, course_name, course_credits, course_details, course_website, Instructor_name, Instructor_email):
            update_course_number(session['U_id'])
            return redirect("Add-Course")
        else:
            connection.rollback()
            return "Error. Course already exists."
        
    if request.method == 'POST' and form_name == "delete-course":
        C_id = request.form.get("C_id")
        del_User(session['U_id'], C_id)
        courses = read_User(session['U_id'])

    return render_template('AddCourse.html', courses = courses, read_data_user=read_data_user)

@app.route("/Mark-Attendance", methods=['GET', 'POST', 'HEAD'])
def Mark_Attendance():
    update_day_tracker(session['U_id'])
    read_data_user = read_userDetails(session['U_id'])
    courses = read_User(session['U_id'])
    date = datetime.today().date()
    fin_day_name=give_day_code(date.strftime("%A"))
    today_attendance = read_day(session['U_id'], fin_day_name)
    done_attendance = read_date_table(session['U_id'])
    attendance_status = check_today_attendance(session['U_id'])

    fin_timetables_list = []
    for i in today_attendance:
        if i not in done_attendance and attendance_status[2] != "MARKED":
            fin_timetables_list.append(i)

    if done_attendance == today_attendance and len(today_attendance) != 0:
        drop_table(session['U_id'], date)
        mark_table(session['U_id'])
        fin_timetables_list=[]

    if request.method == 'POST':
        course_id = request.form.get("form-course-id")
        class_type = request.form.get("form-class-type")
        attendance = request.form.get("attendance")
        day = request.form.get("form-day")
        start_time = request.form.get("form-start-time")
        end_time = request.form.get("form-end-time")
        
        write_User_attendance(session['U_id'], attendance, course_id, class_type)
        write_date_table(session['U_id'], [course_id, class_type, day, start_time, end_time])

        return redirect("Mark-Attendance")
        
    return render_template('MarkAttendance.html', courses=courses, fin_timetables_list=fin_timetables_list, fin_day_name=fin_day_name, read_data_user = read_data_user, date = date)

@app.route("/Today-Schedule", methods=['GET', 'POST', 'HEAD'])
def Schedule():
    read_data_user = read_userDetails(session['U_id'])
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
        C_id = request.form.get("course-id")
        class_type = request.form.get("class-type")
        day = request.form.get("day")

        delete_timetable(session['U_id'], C_id, class_type, day)

        timetables = read_timetable(session['U_id'])
        timetables_list = [item for sublist in timetables for item in sublist]
        courses = read_User(session['U_id'])

    return render_template('Schedule.html', timetables_list=timetables_list, courses=courses, read_data_user=read_data_user)

@app.route("/Analytics", methods=['GET', 'POST', 'HEAD'])
def Course_Analytics():
    read_data_user = read_userDetails(session['U_id'])
    attendance = read_User_attendance(session['U_id'])
    return render_template('Analytics-web.html', attendance=attendance, read_data_user=read_data_user)

@app.route("/Grades", methods=['GET', 'POST', 'HEAD'])
def Grades():
    read_grades_user = read_User_grades(session['U_id'])
    read_data_user = read_userDetails(session['U_id'])
    courses = read_User(session['U_id'])
    form_name = request.form.get('form-name')
    allPermissions = read_grades_table()

    grnated_list = []
    for i in allPermissions:
        if i[2] == "YES":
            grnated_list.append(i)

    grnated_users=[]
    for i in grnated_list:
        temp = read_userDetails(i[0])
        grnated_users.append(temp[0])

    to_show = False
    for i in grnated_list:
        if str(i[0]) == str(session['U_id']):
            to_show = True
            break

    if request.method == 'POST' and form_name=="add-course":
        form_data = request.form
        all_forms_data = []
        Course_id = form_data.get('course-id')
        for key, value in form_data.items():
        # Extract the form index (e.g., from form-course-name-123, we extract 123)
            if key.startswith('assesment-type-'):
                form_index = key.split('-')[-1]
                # Now create a dictionary for this form's data
                form_dict = {
                    form_data.get(f'assesment-type-{form_index}'): form_data.get(f'assesment-weightage-{form_index}')
                }
                all_forms_data.append(form_dict)
        
        final_dict = {}
        for i in all_forms_data:
            final_dict.update(i)

        write_User_grades(session['U_id'], Course_id, final_dict)
        read_grades_user = read_User_grades(session['U_id'])

        return redirect('Grades')
    
    if request.method == 'POST' and form_name == "update-grades":
        course_id = request.form.get("course-id")
        for i in read_grades_user:
            if str(i[0]) == str(course_id):
                for key,value in i[2].items():
                    user_input_num = request.form.get(f"{key}-num")
                    user_input_den = request.form.get(f"{key}-den")
                    if user_input_den != "":
                        i[2][f'{key}'] = str((float(user_input_num)/float(user_input_den))*float(i[1][f'{key}']))
                    else:
                        i[2][f'{key}'] = i[2][f'{key}']
                final_ans = i
                break
        update_user_grades(session['U_id'], final_ans)
        read_grades_user = read_User_grades(session['U_id'])
        sgpa = calculate_sgpa(read_grades_user, courses)
        update_user_grades_table(session['U_id'], sgpa)

        return redirect('Grades')

    return render_template('Grades.html', read_data_user=read_data_user, courses= courses, read_grades_user=read_grades_user, grnated_list=grnated_list, grnated_users=grnated_users, to_show=to_show)

@app.route("/User-Profile", methods=['GET', 'POST', 'HEAD'])
def User_Profile():
    read_data_user = read_userDetails(session['U_id'])

    if request.method == 'POST':
        user_name = request.form.get('User-Name')
        user_name =user_name.title()
        file = request.files['imageInput']
        if file:
            # Secure the filename and save the file to the server
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Generate the URL to the uploaded file
            profile_image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
        else:
            profile_image_url = ""

        if profile_image_url != "":
            update_userDetails(session['U_id'], user_name, profile_image_url)
        else:
            update_userDetails(session['U_id'], user_name, read_data_user[0][4])

        return redirect('Home')

    return render_template('UserProfile.html', read_data_user=read_data_user)

@app.route("/Log-Out", methods=['GET', 'POST', 'HEAD'])
def Logout():
    if request.method == 'POST':
        U_id = request.form.get('delete-Uid')
        U_id = U_id[-4:]
        password = request.form.get('delete-password')
        confirmation = request.form.get('delete-verify')
        existingUsers = read_User_table()

        if confirmation == "DELETE":
            for i in existingUsers:
                if str(i[0]) == str(U_id) and str(U_id) == str(session['U_id']):
                    if str(i[2]) == str(password):
                        session.clear()
                        update_deleted_users(U_id, i[1], password, i[3])
                        delete_User_table(U_id)
                        return redirect('Sign-In')
                    else:
                        return "Incorrect Password"
        else:
            return "type DELETE carefully"
        
    return render_template('Signup.html')

@app.route("/Settings", methods=['GET', 'POST', 'HEAD'])
def Settings():
    all_User_data = read_User_table()
    read_data_user = read_userDetails(session['U_id'])
    all_user_concent = read_grades_table()
    user_concent = ""
    for i in all_user_concent:
        if str(i[0]) == str(session['U_id']):
            user_concent = i[2]

    for i in all_User_data:
        if str(i[0]) == str(session['U_id']):
            Ans = str(i[4])
            break

    if request.method == "POST" :
        concent_value = request.form.get("consent")
        update_concent(session['U_id'], concent_value)
        return redirect('Grades')

    return render_template('settings.html', read_data_user=read_data_user, U_id = Ans, user_concent = user_concent)

@app.route("/sitemap.xml", methods=['GET', 'POST', 'HEAD'])
def Sitemap():
    return send_from_directory('static', 'sitemap.xml')

if __name__ == "__main__":
    app.run(debug=True, port=8000)