from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# from wtforms.fields.html5 import IntegerRangeField
# from io import BytesIO
# import base64


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class tavel_name_form(Form):
    travel_name = StringField('Nombre de tu viaje:', validators=[validators.required()])
    # plazo = TextField('Plazo (años):', validators=[validators.required()])
    # interes = TextField('Interés (TAE, %):', validators=[validators.required()])
    # age = IntegerRangeField('Cantidad (€)', default=90000)

class travel_questionnaire_form(Form):
    question1 = TextAreaField('Primera pregunta para la pipol:', validators=[validators.required()])



@app.route("/", methods=['GET', 'POST'])
def home():
    form = tavel_name_form(request.form)
    print(form.errors)

    if request.method == 'POST':
        travel_name = request.form['travel_name']

        if form.validate():
            # Save the comment here.
            flash('La URL para compartir con tus compañeras de viaje es: ' + request.url + travel_name)
            # print(request.url + travel_name)
            return render_template('home.html', form=form, link=request.url + travel_name)
        else:
            flash('All the form fields are required. ')
            return render_template('home.html', form=form, link=None)

    else:
        return render_template('home.html', form=form, link=None)


@app.route('/<travel_name>')
def show_user_profile(travel_name):
    # show the user profile for that user
    return 'Nombre del viaje: %s' % travel_name


if __name__ == "__main__":
    app.run()