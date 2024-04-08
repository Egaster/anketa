from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
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
        if request.form.get('next'):
            next_id = int(request.form.get('next'))
            answer = 'yes' if next_id == int(questions[int(session['history'][-1])]['next'].get('yes', 0)) else 'no'
            if 'end' in questions[int(session['history'][-1])]['next'] and next_id == int(questions[int(session['history'][-1])]['next']['end']):
                answer = 'end'
            if 'again' in questions[int(session['history'][-1])]['next'] and next_id == int(questions[int(session['history'][-1])]['next']['again']):
                answer = 'again'
            session['answers'][str(session['history'][-1])] = answer
            save_answers_to_database(str(session['history'][-1]), answer)
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
        user_id = session.get('id')  
        if question_id == -2:
            res = html_for_court(session['answers'])
            logging.debug(session['answers'])
        else:
            res = results[int(session['history'][-2])]
        cursor = mysql.connection.cursor()
        print(user_id)
        cursor.execute('SELECT session FROM sessions WHERE uid = %s', (user_id,))
        session_num = cursor.fetchone()
        print(session_num)
        cursor.execute('UPDATE sessions SET session = session + 1 \
                       WHERE uid = %s', (user_id,))
        cursor.execute('DELETE FROM result WHERE id NOT IN (\
                        SELECT MAX(id)\
                        FROM (select * from result) as res \
                        GROUP BY qid, session)')
        mysql.connection.commit()
        cursor.close()
        print(res)
        saved = get_saved_answers_from_database_form(session_num[0])
        print(saved)
        
        return render_template('form.html', question=question, res=res, saved=saved)
    return render_template('form.html', question=question)


def save_answers_to_database(q_id, answer):
    try:
        user_id = session.get('id')  
        print(user_id)
        if user_id == None:
            user_id = 0
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO sessions (uid, session) \
                        SELECT %s, %s \
                        WHERE NOT EXISTS (SELECT * FROM sessions WHERE uid = %s);', (user_id, 1, user_id, ))
        mysql.connection.commit()
        session_number = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT session FROM sessions where uid = %s', (user_id, ))
        session_number = cursor.fetchone()
        cursor.close()
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO result (session, uid, qid, answer) VALUES (%s, %s, %s, %s)', (session_number, user_id, q_id, answer, ))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        app.logger.error(f"Failed to save answers to database: {e}")


def get_saved_answers_from_database_form(session_num):
    try:
        cursor = mysql.connection.cursor()
        user_id = session.get('id')
        if user_id == None:
            user_id = 0
        cursor.execute('SELECT DISTINCT questions.question, text \
                       FROM questions JOIN result ON questions.qid = result.qid \
                       JOIN answers ON result.answer = answers.aid\
                       WHERE result.uid = %s AND result.session = %s', (user_id, session_num, ))
        saved_answers = cursor.fetchall()
        if user_id == 0:
            cursor.execute('DELETE FROM result WHERE uid = 0')
            mysql.connection.commit()
        cursor.close() 
        return saved_answers
    except Exception as e:
        app.logger.error(f"Failed to get saved answers from database: {e}")
        return []

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
    return render_template('judicial_bankruptcy.html')  # Общая информация про судебное или внесудебное


@app.route('/out-of-court_bankruptcy')
def out_of_court_bankruptcy_info():
    return render_template('out-of-court_bankruptcy.html')  # Общая информация про судебное или внесудебное


@app.route('/full_info')
def full_info():
    return render_template('full_info.html')  # Полная инфа после заполнения анкеты и авторизации


@app.route('/profile')
def profile():
    saved = []
    cursor = mysql.connection.cursor()
    user_id = session.get('id')
    cursor.execute('SELECT session\
                    FROM sessions WHERE uid = %s', (user_id,  ))
    num_of_sessions = cursor.fetchall()
    print(num_of_sessions)
    cursor.close() 
    if num_of_sessions != ():
        for i in range(1, num_of_sessions[0][0]):
            saved.append(get_saved_answers_from_database(i))
        return render_template('profile.html', session_data=dict(zip(saved, [x for x in range(1,num_of_sessions[0][0])])))  # Личный кабинет с прошлыми результатами анкеты  # Личный кабинет с прошлыми результатами анкеты
    return render_template('profile.html')

def get_saved_answers_from_database(session_num):
    try:
        cursor = mysql.connection.cursor()
        user_id = session.get('id')
        cursor.execute('SELECT DISTINCT questions.question, text \
                       FROM questions JOIN result ON questions.qid = result.qid \
                       JOIN answers ON result.answer = answers.aid\
                       WHERE result.uid = %s AND result.session = %s', (user_id, session_num, ))
        saved_answers = cursor.fetchall()
        cursor.close() 
        return saved_answers
    except Exception as e:
        app.logger.error(f"Failed to get saved answers from database: {e}")
        return []

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
            return redirect(url_for('home'))
        else:
            msg = 'Неверный логин/пароль!'
    return render_template('sign_in.html', msg=msg)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        hashed_password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM form WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Такой аккаунт уже существует'
        elif not re.match(r'\w+\@\w+.\w{1,3}', username):
            msg = 'Введите корректный адрес электронной почты!'
        elif not username or not hashed_password:
            msg = 'Поля должны быть заполнены!'
        else:
            cursor.execute('INSERT INTO form (`username`, `password`) VALUES (%s, %s)',
                           (username, hashed_password,))
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


@app.route('/sample_declaration_court')
def sample_declaration_court():
    return send_from_directory('/home/user/bankruptcy/static/docs', 'sample_declaration_court.docx', as_attachment=False)


@app.route('/sample_declaration_out_of_court')
def sample_declaration_out_of_court():
    return send_from_directory('/home/user/bankruptcy/static/docs', 'sample_declaration_out_of_court.docx', as_attachment=False)

@app.route('/creditors')
def creditors():
    return send_from_directory('/home/user/bankruptcy/static/docs', 'creditors.docx', as_attachment=False)

def html_for_court(answers):
    html = ''
    if answers['16'] == 'yes':
        html += "<p>При этом, важно учитывать следующий момент: когда Вы узнали (или должны были узнать), что не можете заплатить всем кредиторам, у Вас есть 30 рабочих дней, чтобы подать заявление в суд. Если не успеете, то вам придётся заплатить штраф от 1000 до 3000 рублей (п. 5 <a href='https://www.consultant.ru/document/cons_doc_LAW_34661/cd9e7b3faed04ce5a1863ac280a28ee438df0280/?ysclid=lumge4m3yy484154578', target='_blank'>ст. 14.13 КоАП РФ</a>).</p>"

def html_for_court(answers):
    html = ""
    if '17' in answers and answers['17'] == 'yes':
        html+= "<p>Вы понимаете, что не сможете оплатить долги по всем обязательствам в срок, а это дает Вам возможность открыть процедуру судебного банкротства.</p><p><b>Неплатежеспособность</b> имеет место при соблюдении хотя бы 1 из этих пунктов:<ol class='with-parentheses><li>были прекращены расчеты с кредиторами, то есть Вы перестали исполнять денежные обязательства и (или)  уплачивать обязательные платежи, срок исполнения которых наступил;</li><li>более чем 10% совокупного размера имеющихся у Вас денежных обязательств и (или) обязанности по уплате обязательных платежей, срок исполнения которых наступил, не исполнены Вами в течение более чем 1 месяца со дня, когда такие обязательства и (или) обязанность должны быть исполнены;</li><li>размер Вашей задолженности превышает стоимость имущества, в том числе права требования;</li><li>у Вас есть постановление об окончании исполнительного производства в связи с отсутствием имущества, на которое может быть обращено взыскание.</li><ol>"
    if '18' in answers and answers['18'] == 'no':
        html += "При этом, важно учитывать следующий момент: если у Вас нет имущества, помимо, например, единственного жилья, то у Вас есть право подать в суд заявление о признании банкротом (<a href='https://www.consultant.ru/document/cons_doc_LAW_39331/c2c8c81ee8e4bd843286b08b10607f00ec6ae073/?ysclid=lumgijnp2z11735395' target='_blank'>ст. 213.4 ФЗ «О банкротстве»</a>)."
    if '16' in answers and answers['16'] == 'yes':
        html += "<p>При этом, важно учитывать следующий момент: когда Вы узнали (или должны были узнать), что не можете заплатить всем кредиторам, у Вас есть 30 рабочих дней, чтобы подать заявление в суд. Если не успеете, то вам придётся заплатить штраф от 1000 до 3000 рублей (п. 5 <a href='https://www.consultant.ru/document/cons_doc_LAW_34661/cd9e7b3faed04ce5a1863ac280a28ee438df0280/?ysclid=lumge4m3yy484154578' target='_blank'>ст. 14.13 КоАП РФ</a>).</p>"
    if '10' in answers and answers['10'] == 'no':
        html += "<p>Важно также понимать, что если у Вас нет доказательств того, что Вы не можете оплачивать задолженности вследствие непредвиденных обстоятельств (авария, болезнь, нахождение в больнице, инвалидность, появление нетрудоспособности и т.д.), то суд может не принять заявление или же отказать в признании Вас банкротом в ходе судебного процесса, так как сочтет Ваше поведение недобросовестным (например, когда лицо берет большое количество кредитов, зная заранее, что не будет в состоянии это выплатить). </p>"
    return html
if __name__ == "__main__":
    #app.run(debug=True)
    app.run(debug=False, port=80, host='0.0.0.0')
