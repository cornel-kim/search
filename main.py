import os

from flask import Flask, render_template, request, session, redirect, flash, url_for
import pymysql as pymysql
from werkzeug.utils import secure_filename

# Global connection
app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/coast/PycharmProjects/SCHOOLEXAMS/static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'fghghghghghgrtr'


# UPLOAD_FOLDER = '../static/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def registration():
    # if 'username' in session:
    if request.method == 'POST':
        admission = str(request.form['admission'])
        fullname = str(request.form['fullname'])
        password = str(request.form['password'])
        email = str(request.form['email'])
        standard = str(request.form['standard'])
        phone = str(request.form['phone'])
        gender = str(request.form['gender'])
        age = str(request.form['age'])
        username = str(request.form['username'])
        # profile_pic = request.form['profile_pic']
        # profile_pic.save(secure_filename(profile_pic.filename))

        # #UPLOADING A PHOTO
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # if user does not select file, browser also
        # # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('uploaded_file', filename=filename))
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            conn = pymysql.connect("localhost", 'root', '', 'happy_school')
            cursor = conn.cursor()

            insert_query = "INSERT INTO `registration_table`(`admission`, `fullname`, `password`, `email`, `standard`, `phone`, `gender`, `age`, `username`, `filename`) VALUES  (%s,%s,%s,%s,%s,%s,%s, %s,%s, %s) "

            if insert_query:
                cursor.execute(insert_query, (
                admission, fullname, password, email, standard, phone, gender, age, username, filename,))
                conn.commit()
                # return render_template('registration.html', msg='Registration successful')
                return redirect('/login')

            else:
                conn.rollback()
                return render_template('registration.html', msg='Registration failed')

    else:
        return render_template('registration.html')


# else:
#   return redirect('/login')

# DEF FOR UPLOADING A PHOTO
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # create a connection
        conn = pymysql.connect('localhost', 'root', '', 'happy_school')
        cursor = conn.cursor()

        select_query = "SELECT username, password FROM registration_table WHERE username=%s AND password = %s "
        cursor.execute(select_query, (username, password))
        if cursor.rowcount == 0:
            return render_template('login.html', error_msg='no account found, student do not exist')

        elif cursor.rowcount == 1:
            session['username'] = username
            # return render_template('login.html', success_msg = 'Account found, login succesful')
            return redirect('/Calculation')
        elif cursor.rowcount > 1:
            return render_template('login.html', acc_error='Too many accounts Detected')
        else:
            return render_template('login.html', error='something went wrong')

    else:
        return render_template('login.html')

        # account = cursor.fetchone()
    #     if account:
    #         # session ['login'] = True
    #         session['username'] = account['username']
    #
    #         return render_template('login.html', error_msg='login successfully')
    #
    #     else:
    #         return render_template('login.html', error_msg='something went wrong')
    # else:
    #     return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/Calculation', methods=['POST', 'GET'])
def calculation():
    if 'username' in session:
        if request.method == 'POST':
            fullname = request.form['fullname']
            standard = request.form['standard']
            admission = request.form['admission']
            gender = request.form['gender']
            mathematics = request.form['mathematics']
            english = request.form['english']
            kiswahili = request.form['kiswahili']
            science = request.form['science']
            social = request.form['social']

            # Total_marks = mathematics + english + kiswahili + science + social

            # create a connection
            conn = pymysql.connect('localhost', 'root', '', 'happy_school')
            cursor = conn.cursor()
            sql = "INSERT INTO calculation_table(fullname, standard, admission, gender, mathematics, english, kiswahili, science, social )VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,
                           (fullname, standard, admission, gender, mathematics, english, kiswahili, science, social))

            # sql = "INSERT INTO calculation_table ('fullname', 'standard', 'admission', 'gender', " \
            #                "'mathematics', 'english', 'kiswahili', 'science', 'social') VALUES (%s,%s,%s," \
            #                "%s,%s,%s,%s,%s,%s) "
            # cursor.execute(sql, (fullname, standard, admission, gender, mathematics, english, kiswahili, science, social))
            conn.commit()
            return render_template('calculator.html', msg='Entry successful')
        # else:
        #     conn.rollback()
        #     return render_template('calculator.html', msg='Entry failed')
        else:
            return render_template('calculator.html')
    else:
        return redirect('/login')


def makeConnection():
    return pymysql.connect("localhost", "", "happy_school", )


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        admission = request.form['admission']
        conn = pymysql.connect("localhost", "root", "", "happy_school")
        cursor = conn.cursor()

        cursor.execute("SELECT * from registration_table WHERE admission = %s", admission)
        conn.commit()
        data = cursor.fetchall()
        return render_template('calculator.html', data=data)
    else:
        return render_template('calculator.html')


@app.route('/Students')
def students():
    if 'username' in session:

        conn = pymysql.connect("localhost", "root", "", "happy_school")
        cursor = conn.cursor()

        sql_query = "SELECT * FROM registration_table"
        cursor.execute(sql_query)
        if cursor.rowcount < 1:
            return render_template('students.html', msg='no record found, table is empty')
        else:
            # now we can get all the rows returned by the cursor
            rows = cursor.fetchall()
            # after geting the rows we need
            # to send all of the rows to the UI or the html page
            return render_template('students.html', rows=rows)
    else:
        return redirect('/login')


# @app.route('/check_out', methods=['POST', 'GET'])
# def check_out():
#     if request.method == 'POST':
#         fullname = str(request.form['fullname'])
#
#         # connection to database
#         # the parameters("server","username","password","database")
#         con = pymysql.connect("localhost", "root", "", "happy_school")
#         cursor = con.cursor()
#         sql = "delete from calculation_table where fullname = (%s)"
#         #sql = "UPDATE checkin SET roomno=00 where roomno = (%s)"
#
#         try:
#             # when connection is established successfully
#             cursor.execute(sql, fullname)
#             con.commit()
#             return render_template("check_out.html", msg="You have checked-out successfully")
#         except:
#             # when a connection is not established
#             con.rollback()
#             return render_template("check_out.html", msg="There is a problem with checking-out")
#     else:
#         return render_template("check_out.html")


# @app.route('/regout', methods=['POST', 'GET'])
# def regout():
#     if request.method == 'POST':
#         username = str(request.form['username'])
#
#         # connection to database
#         # the parameters("server","username","password","database")
#         con = pymysql.connect("localhost", "root", "", "siera_project")
#         cursor = con.cursor()
#         sql = "delete from registration_table where username = (%s)"
#
#         try:
#             # when connection is established successfully
#             cursor.execute(sql, username)
#             con.commit()
#             return render_template("regout.html", msg="You have unregistered successfully")
#         except:
#             # when a connection is not established
#             con.rollback()
#             return render_template("regout.html", msg="There is a problem with checking-out")
#     else:
#         return render_template("regout.html")


if __name__ == '__main__':
    app.run(debug=True)

    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
