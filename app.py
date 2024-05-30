import requests
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['RECAPTCHA_SITE_KEY'] = '6LfeguopAAAAAPxB7BQJm1lQUk323UiT5pQcaMfl'
app.config['RECAPTCHA_SECRET_KEY'] = '6LfeguopAAAAAP0GUwH8n6fVtMb6R3OHN9Ct-QCA'
Bootstrap(app)


class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Ваша почта', validators=[DataRequired()])
    message = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


def save_feedback_to_json(feedback_data):
    project_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_directory, 'feedback.json')

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    data.append(feedback_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def verify_recaptcha(response):
    secret_key = app.config['RECAPTCHA_SECRET_KEY']
    payload = {
        'secret': secret_key,
        'response': response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = r.json()
    return result.get('success', False)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Домашняя страница")


@app.route('/examples')
def examples():
    return render_template('examples.html', title="Примеры работ")


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        recaptcha_response = request.form.get('g-recaptcha-response')
        if verify_recaptcha(recaptcha_response):
            feedback_data = {
                'name': form.name.data,
                'email': form.email.data,
                'message': form.message.data
            }
            save_feedback_to_json(feedback_data)
            flash('Feedback submitted successfully!')
        else:
            return redirect(url_for('captcha_failed'))
    return render_template('feedback.html', form=form, title="Обратная связь",
                           recaptcha_site_key=app.config['RECAPTCHA_SITE_KEY'])


@app.route('/captcha_failed')
def captcha_failed():
    return render_template('captcha_failed.html', title="Капча не пройдена")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Страница не найдена"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
