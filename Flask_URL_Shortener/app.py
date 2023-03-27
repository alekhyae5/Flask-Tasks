import os
from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import string 
import random

app=Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
Migrate(app,db)

class urlshort(db.Model):
    __tablename__ = 'urlshorts'
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String())
    urls = db.Column(db.String())
    def __init__(self,url,urls):
        self.url=url
        self.urls=urls
    def __repr__(self):
        return "{} - {}".format(self.url,self.urls)
    
@app.before_first_request
def create_tables():
    db.create_all()

def random_string():
    letters=string.ascii_lowercase+string.ascii_uppercase+string.digits
    while True:
        rand_string=random.choices(letters,k=3)
        rand_string="".join(rand_string)
        shorturl=urlshort.query.filter_by(urls=rand_string).first()
        if not shorturl:
            return rand_string

@app.route('/',methods=['POST','GET'])
def home():
    if request.method=="POST":
        url=request.form.get('url_in')
        found_url=urlshort.query.filter_by(url=url).first()
        if found_url:
            return redirect(url_for("display",url=found_url.urls))
        else:
            urls=random_string()
            new_urls=urlshort(url,urls)
            db.session.add(new_urls)
            db.session.commit()
            return redirect(url_for("display",url=urls))
    return render_template('home.html')

@app.route('/<urls>')
def redirction(urls):
    original_url=urlshort.query.filter_by(urls=urls).first()
    if original_url:
        return redirect(original_url.url)
    else:
        return f'<h1>Url does not exist</h1>'

@app.route('/display<url>')
def display(url):
    return render_template('home.html',short_url_display=url)

@app.route('/history')
def history():
    urlshort_url=urlshort.query.all()
    return render_template('history.html',urlshorts=urlshort_url)

def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    
@app.route('/clear')
def clear():
    clear_data()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
