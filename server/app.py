#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
                    #this is not  fully functional app. User interface/rendered web page doesnt suppossed to work. It is just for this exercise/lab
@app.route('/clear') #setting a new session. giving client another 3 attempts
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')  #getting all the articles. According to the lab the client won't be allowed to use this. get request
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return make_response(jsonify(articles), 200)

@app.route('/articles/<int:id>')   # limiting the client to 3 get requests
def show_article(id):

    session['page_views'] = session.get('page_views') or 0
    session['page_views'] += 1

    if session['page_views'] <= 3:
        return Article.query.filter(Article.id == id).first().to_dict(), 200
        
    return {'message': 'Maximum pageview limit reached'}, 401
    

if __name__ == '__main__':
    app.run(port=5555)
