from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt
from functools import wraps
import requests
import mysql.connector

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim Soyisim", validators=[validators.Length(min=4, max=25)])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=5, max=35)])
    email = StringField("Email Adresi", validators=[validators.Email(message="Lütfen geçerli bir email adresi girin!")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen bir parola belirleyin!"),
        validators.EqualTo(fieldname="confirm", message="Parolanız uyuşmuyor!")
    ])
    confirm = PasswordField("Parola Doğrula")

#Kullanıcı Giriş Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")



app = Flask(__name__)
app.secret_key = "project"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] =""
app.config["MYSQL_DB"] = "project"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

api_key = "cd72899202fc4fc3eeccc95c747c6f97"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def get_weather():
    city = request.form['city']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    if response.status_code == 200:
        weather = {
            'description': weather_data['weather'][0]['description'],
            'temperature': weather_data['main']['temp'],
            'city': weather_data['name'],
            'country': weather_data['sys']['country']
        }
        return render_template('weather.html', weather=weather)
    else:
        flash("Böyle bir şehir bulunamadı.","danger")
        return redirect(url_for("index"))
    
@app.route("/register", methods= ["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()
        sorgu = "Insert into users(name,username,email,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(sorgu,(name,username,email,password))
        mysql.connection.commit()
        cursor.close()

        flash("Başarıyla Kayıt Oldunuz.","success")
        return redirect(url_for("index"))
    else:
        return render_template("register.html", form = form)
    
@app.route("/login", methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        sorgu = "Select * From users where username = %s"
        result = cursor.execute(sorgu,(username,))
        
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered, real_password):
                flash("Başarıyla Giriş Yapıldı.","success")
                session["logged_in"] = True
                session["username"] = username
                update_score = (
                "UPDATE users SET score = 0 WHERE username = %s"
                )
                cursor.execute(update_score, (username,))
                cursor.connection.commit()
                return redirect(url_for("index"))
            else:
                flash("Parolanızı Yanlış Girdiniz!","danger")
                return redirect(url_for("login"))
        else:
            flash("Böyle Bir Kullanıcı Bulunmuyor!","danger")
            return redirect(url_for("login"))
        
        

    return render_template("login.html", form = form) 

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

def append_answered_questions(question_id, status, session):
    answer_status = (question_id, status)
    answered_questions = session["answered_questions"]
    answered_questions.append(answer_status)
    session["answered_questions"] = answered_questions


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM questions ORDER BY RAND()"
    cursor.execute(sorgu)
    questions: tuple = cursor.fetchall()
    question_list = list(questions)

    if "answered_questions" not in session:
        session["answered_questions"] = []

    tuples = session["answered_questions"]
    answer_questions_ids = [item[0] for item in tuples]
    print(answer_questions_ids)
    for question in questions:
        if str(question["id"]) in answer_questions_ids:
            question_list.remove(question)
    if len(question_list) <= 0:
        return redirect(url_for("index"))

    if request.method == "POST":
        question_id = request.form["id"]

        if len(request.form) <= 1:
            append_answered_questions(question_id, None, session=session)
            return redirect(url_for("quiz"))

        user_answer = request.form[question_id]

        for question in question_list:
            if int(question_id) == int(question["id"]):
                correct_answer = question["correct_option"]

        status = True if int(user_answer) == int(correct_answer) else False
        append_answered_questions(question_id, status, session=session)
        username = session["username"]
        print(username)
        if status:
            update_score = (
                "UPDATE users SET score = score + 10 WHERE username = %s"
            )
            cursor.execute(update_score, (username,))
            cursor.connection.commit()
        print(
            f"Cevaplanmış Soru ID: {question_id}, Verilen cevap: {user_answer}, Doğru Cevap: {correct_answer}, Durum: {status}"
        )

        return redirect(url_for("quiz"))

    return render_template("quiz.html", questions=question_list)

@app.route("/leaderboard")
def leaderboard():
    cursor = mysql.connection.cursor()
    sorgu = "SELECT * FROM users ORDER BY `users`.`score` DESC"
    result = cursor.execute(sorgu)
    users = cursor.fetchall()
    return render_template("leaderboard.html", users = users)

@app.route("/addquestion", methods = ["GET", "POST"])
def addquestion():
    form = AddForm(request.form)
    if request.method == "POST":
        question_text = form.question_text.data
        option1 = form.option1.data
        option2 = form.option2.data
        option3 = form.option3.data
        option4 = form.option4.data
        correct_option = form.correct_option.data

        cursor = mysql.connection.cursor()
        sorgu = "Insert into questions(question_text, option1, option2, option3, option4, correct_option) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sorgu,(question_text,option1,option2,option3,option4,correct_option,))
        mysql.connection.commit()
        cursor.close()

        flash("Soru başarıyla eklendi.", "success")


    return render_template("addquestion.html", form = form)

class AddForm(Form):
    question_text = TextAreaField("Soru")
    option1 = StringField("1. Seçenek")
    option2 = StringField("2. Seçenek")
    option3 = StringField("3. Seçenek")
    option4 = StringField("4. Seçenek")
    correct_option = IntegerField("Doğru seçeneğin index numarası")





   



if __name__ == "__main__":
    app.run(debug=True)
