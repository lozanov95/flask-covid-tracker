from app import app
from flask import render_template, flash, redirect, url_for, request
from app.scrape_cases import CaseScrapper
from datetime import datetime
from app.models import Cases, User
from app import db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    covid_stats = Cases.query.order_by(Cases.date.desc())
    return render_template('index.html', covid_stats=covid_stats)


@login_required
@app.route('/scrape')
def scrape():
    scrapper = CaseScrapper()
    cases, tests = scrapper.get_stats()
    positive = round(cases / tests * 100, 2)
    date = datetime.utcnow().date()
    cases_object = Cases(date=date, cases=cases, tests=tests, positive=positive)
    try:
        db.session.add(cases_object)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


"""
@app.route('/test')
def test():
    return str(datetime.utcnow().date())
"""