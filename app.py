import json
import logging.config
import os
from urllib.parse import urljoin


import requests
from feedgen.feed import FeedGenerator
from flask import (Blueprint, Flask, jsonify, make_response, redirect,
                   render_template, request, url_for)
from flask_bootstrap import Bootstrap
from werkzeug.contrib.atom import AtomFeed



app = Flask(__name__)
Bootstrap(app)



def get_abs_url(url):
    """ Returns absolute url by joining post url with base url """
    return urljoin(request.url_root, url)


@app.route('/feeds/')
def feeds():
    feed = AtomFeed(title='All Advertisements feed',
                    feed_url=request.url, url=request.url_root)

    response = requests.get("https://fa-project2.azurewebsites.net/api" + '/getAdvertisements')
    posts = response.json()

    for key, value in posts.items():
        print("key,value: " + key + ", " + value)

    #     feed.add(post.title,
    #              content_type='html',
    #              author= post.author_name,
    #              url=get_abs_url(post.url),
    #              updated=post.mod_date,
    #              published=post.created_date)

    # return feed.get_response()


@app.route('/rss')
def rss():
    fg = FeedGenerator()
    fg.title('Feed title')
    fg.description('Feed Description')
    fg.link(href='https://neighborly-client-v1.azurewebsites.net/')
    

    response = requests.get("https://fa-project2.azurewebsites.net/api" + '/getAdvertisements')
    ads = response.json()

    for a in ads: 
        fe = fg.add_entry()
        fe.title(a.title)
        fe.description(a.description)

    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')
    return response

@app.route('/')
def home():
    response = requests.get("https://fa-project2.azurewebsites.net/api" + '/getAdvertisements')
    response2 = requests.get("https://fa-project2.azurewebsites.net/api" + '/getPosts')

    ads = response.json()
    posts = response2.json()
    return render_template("index.html", ads=ads, posts=posts)


@app.route('/ad/add', methods=['GET'])
def add_ad_view():
    return render_template("new_ad.html")


@app.route('/ad/edit/<id>', methods=['GET'])
def edit_ad_view(id):
    response = requests.get("https://fa-project2.azurewebsites.net/api" + '/getAdvertisement?id=' + id)
    ad = response.json()
    return render_template("edit_ad.html", ad=ad)


@app.route('/ad/delete/<id>', methods=['GET'])
def delete_ad_view(id):
    response = requests.get("https://fa-project2.azurewebsites.net/api" + '/getAdvertisement?id=' + id)
    ad = response.json()
    return render_template("delete_ad.html", ad=ad)

@app.route('/ad/view/<id>', methods=['GET'])
def view_ad_view(id):
    response = requests.get("https://fa-project2.azurewebsites.net/api" + '/getAdvertisement?id=' + id)
    ad = response.json()
    return render_template("view_ad.html", ad=ad)

@app.route('/ad/new', methods=['POST'])
def add_ad_request():
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }
    response = requests.post("https://fa-project2.azurewebsites.net/api" + '/createAdvertisement', json=json.dumps(req_data))
    return redirect(url_for('home'))

@app.route('/ad/update/<id>', methods=['POST'])
def update_ad_request(id):
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }
    response = requests.put("https://fa-project2.azurewebsites.net/api" + '/updateAdvertisement?id=' + id, json=json.dumps(req_data))
    return redirect(url_for('home'))

@app.route('/ad/delete/<id>', methods=['POST'])
def delete_ad_request(id):
    response = requests.delete("https://fa-project2.azurewebsites.net/api" + '/deleteAdvertisement?id=' + id)
    if response.status_code == 200:
        return redirect(url_for('home'))

# running app
def main():
    print(' ----->>>> Flask Python Application running in development server')
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
