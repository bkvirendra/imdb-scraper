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
        hxs = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/" + request.args.get("id")).content )
        media_index = lxml.html.document_fromstring(requests.get("http://www.imdb.com/title/"+ request.args.get("id")).content +"/mediaindex")
        movie = {}
        try:
            movie['title'] = hxs.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/h1/text()')[0].strip()
        except IndexError:
            movie['title'] = ""
        try:
            movie['year'] = hxs.xpath('//*[@id="titleYear"]/a/text()')[0].strip()
        except IndexError:
            movie['year'] = ""
        try:
            movie['certification'] = hxs.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/meta/text()')[0].strip()
        except IndexError:
            movie['certification'] = ""
        try:
            movie['running_time'] = hxs.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/time/@datetime')[0].strip()
        except IndexError:
            movie['running_time'] = ""
        try:
            movie['genre'] = hxs.xpath('//*[@id="titleStoryLine"]/div[3]/a/text()')
        except IndexError:
            movie['genre'] = []
        try:
            release_date = hxs.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/div/a[4]/text()')[0].strip()
            movie['release_date'] = release_date
        except IndexError:
            movie['release_date'] = ""
        try:
            movie['rating'] = hxs.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')[0]
        except IndexError:
            movie['rating'] = ""
        try:
            movie['metascore'] = hxs.xpath('//*[@id="title-overview-widget"]/div[3]/div[2]/div[1]/a/div/span/text()')[0].strip()[0]
        except IndexError:
            movie['metascore'] = 0
        try:
            movie['description'] = hxs.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[1]/text()')[0].strip()
        except IndexError:
            movie['description'] = ""
        try:
            movie['director'] = hxs.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[2]/span/a/span/text()')[0].strip()
        except IndexError:
            movie['director'] = ""
        try:
            movie['stars'] = hxs.xpath('//*[@id="overview-top"]/div[6]/a/span/text()')
        except IndexError:
            movie['stars'] = ""
        try:
            movie['poster'] = hxs.xpath('//*[@id="title-overview-widget"]/div[2]/div[3]/div[1]/a/img/@src')[0]
        except IndexError:
            movie['poster'] = ""
        try:
            movie['gallery'] = media_index.xpath('///*[@id="media_index_thumbnail_grid"]/a/img/@src')
        except IndexError:
            movie['gallery'] = ""
        try:
            movie['storyline'] = hxs.xpath('//*[@id="titleStoryLine"]/div[1]/p/text()')[0].strip()
        except IndexError:
            movie['storyline'] = ""

        cast= []
        for actor in hxs.xpath('//*[@id="title-overview-widget"]/div[3]/div[1]/div[4]/span/a'):
            cast_raw = {}
            cast_raw['name'] = actor.xpath('.//span/text()')[0]
            cast_raw['link'] = actor.xpath('.//@href')[0]
            cast.append(cast_raw)
        movie['cast'] = cast
    else:
        return "invalid id"
    return jsonify(movie)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)