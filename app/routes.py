from app import app
from flask import render_template, url_for
from app.scrape_cases import CaseScrapper
from datetime import datetime
from app.models import Cases
from app import db


@app.route('/')
@app.route('/index')
def index():
    covid_stats = Cases.query.all()
    return render_template('index.html', covid_stats=covid_stats)


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
        covid_stats = Cases.query.all()
        return render_template('index.html', covid_stats=covid_stats)


@app.route('/test')
def test():
    return str(datetime.utcnow().date())