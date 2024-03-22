from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)
 
@app.route('/')
def home():
    return render_template('home.html')  # Главная

@app.route('/info')
def info():
    return render_template('info.html') # Общая информация про судебное или внесудебное
                                        

@app.route('/full_info')
def full_info():
    return render_template('full_info.html') # Полная инфа после заполнения анкеты и авторизации

@app.route('/profile')
def profile():
    return render_template('profile.html') # Личный кабинет с прошлыми результатами анкеты

@app.route('/settings')
def settings():
    return render_template('settings.html') # Настройки

@app.route('/sign-in')
def sign_in():
    return render_template('sign_in.html') # Страница входа с вводом логина и пароля

@app.route('/sign-up')
def sign_up():
    return render_template('sign_up.html')  # Страница регистрации

if __name__ == "__main__":
    app.run(debug=True)