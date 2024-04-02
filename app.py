from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import hashlib
import json
import logging

app = Flask(__name__)
app.secret_key = ' key'
app.logger.setLevel(logging.DEBUG)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'LOGIN'


mysql = MySQL(app)


with open('questions.json', 'r', encoding='utf8') as f:
    data = json.load(f)
questions = {q['id']: q for q in data['Questions']}


with open('results.json', 'r', encoding='utf8') as f:
    data = json.load(f)
results = {r['id']: r for r in data['Results']}


@app.route('/form', methods=['GET', 'POST'])
def form():
    if 'history' not in session:
        session['history'] = []
    if 'answers' not in session:
        session['answers'] = {}

    if request.method == 'POST':
        next_id = int(request.form.get('next'))
        answer = 'yes' if next_id == int(questions[int(session['history'][-1])]['next']['yes']) else 'no'
        session['answers'][str(session['history'][-1])] = answer
        session['history'].append(str(next_id))
        session.modified = True
    else:
        question_id = int(request.args.get('question_id', 1))
        if str(question_id) not in session['history']:
            session['history'].append(str(question_id))
        session.modified = True

    question_id = int(session['history'][-1])
    question = questions[question_id]
    if question_id < 0:
        print(session['history'])
        res = results[int(session['history'][-2])]
        return render_template('form.html', question=question, res=res)
    return render_template('form.html', question=question)

@app.route('/back', methods=['GET'])
def back():
    if len(session['history']) > 1:  
        session['history'].pop()  
        session.modified = True
    return redirect(url_for('form', question_id=session['history'][-1]))

@app.route('/')
def home():
    if 'history' in session:
        session['history'] = []
    if 'answers' in session:
        session['answers'] = {}
    return render_template('home.html')  # Главная

@app.route('/need')
def need():
    return render_template('need.html')  # Главная


@app.route('/judicial_bankruptcy')
def judicial_bankruptcy_info():
    return render_template('judicial_bankruptcy.html') # Общая информация про судебное или внесудебное
                                        
@app.route('/out-of-court_bankruptcy')
def out_of_court_bankruptcy_info():
    return render_template('out-of-court_bankruptcy.html') # Общая информация про судебное или внесудебное

@app.route('/full_info')
def full_info():
    return render_template('full_info.html')  # Полная инфа после заполнения анкеты и авторизации


@app.route('/profile')
def profile():
    return render_template('profile.html')  # Личный кабинет с прошлыми результатами анкеты


@app.route('/settings')
def settings():
    return render_template('settings.html')  # Настройки

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        hashed_password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM form WHERE username = %s AND password = %s', (username, hashed_password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # msg = 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            msg = 'Неверный логин/пароль!'
    return render_template('sign_in.html', msg=msg)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'phone' in request.form:
        username = request.form['username']
        hashed_password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        phone = request.form['phone']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM form WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Такой аккаунт уже существует'
        elif not re.match(r'(\+7|8)\d{10}', phone):
            msg = 'Введите корректный номер телефона!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Логин может содержать только буквы и цифры!'
        elif not username or not hashed_password or not phone:
            msg = 'Поля должны быть заполнены!'
        else:
            cursor.execute('INSERT INTO form (`username`, `password`, `phone`) VALUES (%s, %s, %s)', (username, hashed_password, phone,))
            mysql.connection.commit()
            msg = 'Регистрация прошла успешно!'
            return redirect(url_for('home'))
    elif request.method == 'POST':
        msg = 'Поля должны быть заполнены!'
    return render_template('sign_up.html', msg=msg)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('loggedin', None)
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
