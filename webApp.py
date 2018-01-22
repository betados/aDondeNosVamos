from flask import Flask, render_template, flash, request
from wtforms import Form, TextAreaField, validators, StringField, PasswordField
import random
import sqlite3


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class tavel_name_form(Form):
    travel_name = StringField('Nombre de tu viaje:', validators=[validators.required()])
    password = PasswordField('Contraseña:  ', validators=[validators.required()])
    password2 = PasswordField('Repite la contraseña:', validators=[validators.required()])


class travel_questionnaire_form(Form):
    user_name = StringField('Tu nombre:', validators=[validators.required()])
    question1 = TextAreaField('Primera pregunta para la pipol:', validators=[validators.required()])
    question2 = TextAreaField('Segunda pregunta para la pipol:', validators=[validators.required()])


def createUrl():
    url = ''
    for _ in range(9):
        code = random.randrange(36)
        if code in range(10):
            code += 48
        elif code in range(10, 36):
            code += 87
        url += chr(code)
    return url


def createTravel(name, password, url):
    conn = sqlite3.connect('dataBases/viajes.db')
    c = conn.cursor()
    values = (name, password, url)
    c.execute('create table if not exists viajes(name, password, url)')
    c.execute('insert into viajes values (?,?,?)', values)
    conn.commit()


def saveAnswer(url, travel_name, user_name, respuesta):
    conn = sqlite3.connect('dataBases/viajes.db')
    c = conn.cursor()
    values = (url, travel_name, user_name, respuesta)
    c.execute('create table if not exists respuestas(url, travel_name, user_name, respuesta)')
    c.execute('insert into respuestas values (?,?,?,?)', values)
    conn.commit()


@app.route("/", methods=['GET', 'POST'])
def home():

    form = tavel_name_form(request.form)
    print(form.errors)

    if request.method == 'POST':
        travel_name = request.form['travel_name']
        password = request.form['password']
        password2 = request.form['password2']

        if form.validate():
            if password == password2:
                url = createUrl()
                flash('La URL para compartir con tus compañeras de viaje es: ' + request.url + url)
                createTravel(travel_name, password, url)
                return render_template('home.html', form=form, link=request.url + url)
            else:
                flash('Las contraseñas no coinciden')
                return render_template('home.html', form=form, link=None)
        else:
            flash('All the form fields are required. ')
            return render_template('home.html', form=form, link=None)

    else:
        return render_template('home.html', form=form, link=None)


@app.route('/<url>', methods=['GET', 'POST'])
def show_questionnaire(url):
    conn = sqlite3.connect('dataBases/viajes.db')
    c = conn.cursor()
    values = (url,)
    c.execute('SELECT name FROM viajes WHERE url=?', values)
    try:
        travel_name = c.fetchone()[0]
    except:
        return render_template('404.html')

    from flask import request


    admin = request.args.get('admin', type=bool)
    if admin:
        # TODO hacer que pida la contraseña para acceder a esto
        conn = sqlite3.connect('dataBases/viajes.db')
        c = conn.cursor()
        values = (travel_name,)
        c.execute('SELECT * FROM respuestas WHERE travel_name=?', values)
        query_result = c.fetchall()
        # [0]
        return render_template('results.html', travel_name=travel_name, query_result=query_result)

    form = travel_questionnaire_form(request.form)
    # flash('Nombre del viaje: %s' % travel_name)

    if request.method == 'POST':
        user_name = request.form['user_name']
        q1 = request.form['question1']
        q2 = request.form['question2']

        if form.validate():
            saveAnswer(url, travel_name, user_name, q1 + ' - ' + q2)

    return render_template('questionnaire.html', form=form, travel_name=travel_name, url=url)


if __name__ == "__main__":
    app.run()
