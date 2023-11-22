from flask import Flask, url_for, render_template, request, redirect, session
import pyodbc 
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        if username == '':
            return render_template('login.html')
        hash_pwd = generate_password_hash(pwd)
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=OLALA;DATABASE=DB_WEB_ENGLISH;')
        cusor = conn.cursor()
        cusor.execute(f"SELECT UserName, PassWord FROM User1 WHERE CAST(UserName AS varchar(MAX)) = '{username}'")
        user = cusor.fetchone()
        cusor.close()
        if user and check_password_hash(user[1], pwd) == True:
            return render_template('home.html', username  = user[0])
        else:
            return render_template('login.html', error = 'Sai thông tin đăng nhập')
    return render_template('login.html')

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        sex = request.form['sex']
        pwd = request.form['password']
        print(name, username, sex, pwd)
        hashed_pwd = generate_password_hash(pwd)
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=OLALA;DATABASE=DB_WEB_ENGLISH;')
        cusor = conn.cursor()
        cusor.execute(f"SELECT Name FROM User1 WHERE UserName = '{username}'")
        user_check = cusor.fetchone()
        if user_check != '':
            return render_template('registration.html', error = 'Nickname đã được đăng ký, vui lòng chọn tên khác')
        
        cusor.execute(f"INSERT INTO User1 (Name, UserName, SEX, PassWord) VALUES ('{name}', '{username}', '{sex}','{hashed_pwd}')")
        conn.commit()
        return render_template('login.html')
    return render_template('registration.html')

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/new_word', methods = ['GET', 'POST'])
def new_word(username):
    if request.method == 'POST':
        word = request.form['word']
        meaning = request.form['meaning']
        wordType = request.form['wordType']
        sentence = request.form['sentence']
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=OLALA;DATABASE=DB_WEB_ENGLISH;')
        cusor = conn.cursor()
        cusor.execute(f"INSERT INTO NewWord (word, meaning, wordType, sentence) VALUES ('{word}', '{meaning}', '{wordType}','{sentence}')")
        conn.commit()
    return render_template('New_word.html')
def get_word():
    if request.method == 'GET':
        result= []
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=OLALA;DATABASE=DB_WEB_ENGLISH;')
        cusor = conn.cursor()
        cusor.execute(f"Select * from NewWord")
        for row in cusor.fetchall():
            item_dict = {}
            item_dict["word"] = row[1]
            item_dict["meaning"] = row[2]
            item_dict["wordType"] = row[3]
            item_dict["sentence"] = row[4]
        return render_template('New_word.html', result)
# @app.route('/get_word', methods = ['GET', 'POST'])
# def get_word():
#     if request.method == 'GET':
#         result= []
#         conn = pyodbc.connect('DRIVER={SQL Server};SERVER=OLALA;DATABASE=DB_WEB_ENGLISH;')
#         cusor = conn.cursor()
#         cusor.execute(f"Select * from NewWord")
#         for row in cusor.fetchall():
#             item_dict = {}
#             item_dict["word"] = row[1]
#             item_dict["meaning"] = row[2]
#             item_dict["wordType"] = row[3]
#             item_dict["sentence"] = row[4]
#         return render_template(, )
        



if __name__ == "__main__":
    app.run(debug=True)