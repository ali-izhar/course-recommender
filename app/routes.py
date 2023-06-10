import os
import re
import string
import json
import openai
import requests
import nltk
from nltk import PorterStemmer

from nltk.corpus import wordnet, stopwords
from dotenv import load_dotenv
from flask import render_template, request, make_response, redirect, url_for, jsonify, flash
from urllib.parse import unquote
from app import app, db
from model.model import Recommender
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import  login_user, login_required, logout_user, current_user

# Machine Learning Model
ML_MODEL = Recommender()

load_dotenv()

try:
    nltk.data.find('corpora/wordnet')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download(['wordnet', 'stopwords'], quiet=True)

ps = PorterStemmer()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['firstName']
        password1 = request.form['password1']
        password2 = request.form['password2']

        user = User.query.filter_by(email=email).first()

        if user:
            flash('User Account already exists!', category='error')
        elif len(password1) < 8:
            flash('Password should contain at least 8 characters!', category='error')
        elif password1 != password2:
            flash("The passwords don't match!", category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('index'))

    return render_template('signup.html', user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('index'))
            else:
                flash('Invalid password!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template("login.html", user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    """ Default webpage."""
    return render_template("index.html", user=current_user)


@app.route('/about')
def about():
    """ About webpage."""
    return render_template("about.html",user=current_user)


@app.route('/options', methods=['POST'])
def options():
    """ Options webpage. Get the user's input and return the results from the Udemy API."""
    title = request.form.get("title")

    title = clean_input(title)
    if not title or not validate_input(title):
        return render_template("result_api.html", source="API", choices="", type="error", user=current_user)

    names = "https://udemy-course-scrapper-api.p.rapidapi.com/course-names"
    urls = "https://udemy-course-scrapper-api.p.rapidapi.com/course-names/course-instructor/course-url"
    headers = {
        "X-RapidAPI-Key": os.getenv("COURSE_API_KEY"),
        "X-RapidAPI-Host": os.getenv("COURSE_API_HOST")
    }
    choices = []

    titles = requests.request("GET", names, headers=headers)
    links = requests.request("GET", urls, headers=headers)

    tokens = remove_stopwords(title).strip().lower().split()
    if titles.status_code == 200 and links.status_code == 200:
        titles = titles.json().values()
        links = links.json().values()
        for i, j in zip(titles, links):
            course_title = remove_stopwords(i['course_name']).strip().lower().split()

            # check if more than half of the tokens are in the course title
            count = 0
            for word in tokens:
                if word in course_title:
                    count += 1
            if count >= len(tokens) / 2:
                choices.append([i['course_name'], j['course url']])

    suggestions = get_suggestions(title)
    favorite_courses = []
    for note in current_user.notes:
        favorite_courses.append(note.data)
    return render_template("result_api.html", source="API", choices=choices, suggestions=suggestions,
                           favorites = favorite_courses, type="list", user=current_user)


@app.route('/model', methods=['POST'])
def model_result():
    """ Model webpage. Get the user's input and return the results from the model."""
    prompt = request.form.get("prompt")
    prompt = clean_input(prompt)
    if not prompt or not validate_input(prompt):
        return render_template("result_ml.html", source="ML", choices="", type="error", user=current_user)
    choices = ML_MODEL.recommend_course(prompt)
    choices = [[k, v['url']] for k, v in choices]
    return render_template("result_ml.html", source="ML", choices=choices, type="list", user=current_user)


@app.route('/result', methods=['POST'])
def chatbot_result():
    """ Get results from ChatGPT model based on user's input."""
    prompt = request.form.get("prompt")
    prompt = clean_input(prompt, r_stopwords=False)
    if not prompt or not validate_input(prompt):
        return render_template("result_gpt.html", source="GPT", choices="", type="error", user=current_user)
    chat = get_chatbot_results(prompt)
    return render_template("result_gpt.html", source="GPT", choices=chat, type="string", user=current_user)


def get_chatbot_results(prompt):
    """ Get text output from the model."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model_engine = "text-davinci-002"
    try:
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=3500,        # prompt + response = x + 3500 <= 4096 limit
            n=3,                    # number of responses
            stop=None,
            temperature=0.7
        )
        messages = [choice.text for choice in response['choices']]
        message = ' '.join(messages)
    except openai.error.RateLimitError:
        return "Maximum number of requests reached. Please try again later."
    return message.strip().splitlines()


def get_suggestions(title):
    prompt_format = "#; Course Name; Course URL"
    prompt = f"Suggest 5 courses that are related to {title} in the following format {prompt_format}"
    results = get_chatbot_results(prompt)
    suggestions = []
    for i in results:
        if i != '':
            suggestions.append(i.split(';')[1:])
    return suggestions


@app.route('/external/<path:choice>')
def external(choice):
    """ Redirect to the external link for the selected course."""
    decoded_choice = unquote(choice)
    response = make_response('', 302)
    response.headers['Location'] = decoded_choice
    return response


@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'POST':
        returned = request.form.get("listOption").split("\', \'")
        name, address = returned[0][2:], returned[1][:-2]
        for i in range(0, db.session.query(Note).count()):
            try:
                if Note.query.get(str(i + 1)).data == name:
                     return render_template("favorites.html", type="list", user=current_user)
            except AttributeError:
                print("AttributeError")
        new_note = Note(data=name, url=address, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('favorites'))
    else:
        return render_template("favorites.html", type="list", user=current_user)


@app.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})


def validate_input(user_input):
    """ Check if the sentence is valid."""

    tokens = user_input.split()

    # Remove duplicates
    tokens = list(set(tokens))

    # Check if the input contains mostly numbers
    num_count = sum(c.isdigit() for c in user_input)
    if num_count >= len(user_input) * 0.75:
        return False

    # Check if the input contains mostly punctuation marks
    punct_count = sum(c in string.punctuation for c in user_input)
    if punct_count >= len(user_input) * 0.75:
        return False

    # Check if the input contains mostly non-English words
    non_english_count = sum(not wordnet.synsets(word) for word in tokens)
    if non_english_count >= len(tokens) * 0.75:
        return False

    return True

def clean_input(prompt, r_stopwords=True):
    """ Clean the prompt."""
    prompt = prompt.strip()
    if not prompt:
        return ""

    prompt = prompt.lower()
    prompt = re.sub(r'[^\w\s]', '', prompt)
    if r_stopwords:
        prompt = remove_stopwords(prompt)
    return prompt


def remove_stopwords(sentence):
    """ Remove stopwords from the sentence."""
    tokens = sentence.split()
    tokens = [token.translate(str.maketrans('', '', string.punctuation)) for token in tokens]
    filtered_sentence = [token for token in tokens if token not in stopwords.words('english')]
    return ' '.join(filtered_sentence)