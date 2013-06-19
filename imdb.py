#!/usr/bin/env python

import os
import requests
import lxml.html

from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get/')
def get():
    if request.args.get("id") is not None and request.args.get("id").startswith('tt'):
        hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + request.args.get("id")).content)
        movie = {}
        try:
            movie['title'] = hxs.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0].strip()
        except IndexError:
            movie['title']
        try:
            movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[2]/a/text()')[0].strip()
        except IndexError:
            try:
                movie['year'] = hxs.xpath('//*[@id="overview-top"]/h1/span[3]/a/text()')[0].strip()
            except IndexError:
                movie['year'] = ""
        try:
            movie['certification'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[1]/@title')[0].strip()
        except IndexError:
            movie['certification'] = ""
        try:
            movie['running_time'] = hxs.xpath('//*[@id="overview-top"]/div[2]/time/text()')[0].strip()
        except IndexError:
            movie['running_time'] = ""
        try:
            movie['genre'] = hxs.xpath('//*[@id="overview-top"]/div[2]/a/span/text()')
        except IndexError:
            movie['genre'] = []
        try:
            movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[3]/a/text()')[0].strip()
        except IndexError:
            try:
                movie['release_date'] = hxs.xpath('//*[@id="overview-top"]/div[2]/span[4]/a/text()')[0].strip()
            except Exception:
                movie['release_date'] = ""
        try:
            movie['rating'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/strong/span/text()')[0]
        except IndexError:
            movie['rating'] = ""
        try:
            movie['metascore'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[2]/text()')[0].strip().split('/')[0]
        except IndexError:
            movie['metascore'] = 0
        try:
            movie['description'] = hxs.xpath('//*[@id="overview-top"]/p[2]/text()')[0].strip()
        except IndexError:
            movie['description'] = ""
        try:
            movie['director'] = hxs.xpath('//*[@id="overview-top"]/div[4]/a/span/text()')[0].strip()
        except IndexError:
            movie['director'] = ""
        try:
            movie['stars'] = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
        except IndexError:
            movie['stars'] = ""
        try:
            movie['poster'] = hxs.xpath('//*[@id="img_primary"]/div/a/img/@src')[0]
        except IndexError:
            movie['poster'] = ""
        try:
            movie['gallery'] = hxs.xpath('//*[@id="combined-photos"]/div/a/img/@src')
        except IndexError:
            movie['gallery'] = ""
        try:
            movie['storyline'] = hxs.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')[0].strip()
        except IndexError:
            movie['storyline'] = ""
        try:
            movie['votes'] = hxs.xpath('//*[@id="overview-top"]/div[3]/div[3]/a[1]/span/text()')[0].strip()
        except IndexError:
            movie['votes'] = ""
    else:
        return "invalid id"
    return jsonify(movie)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)