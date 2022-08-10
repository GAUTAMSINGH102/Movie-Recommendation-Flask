from flask import Flask, render_template, request

import pandas as pd
import numpy as np

# Importing Class
import ContentBased
import CollaborativeBased

# Creating Object of Class
objectContentBased = ContentBased.ContentBasedClass()
objectCollaborativeBased = CollaborativeBased.CollaborativeBasedClass()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/user')
def user():
    return render_template("user.html")


@app.route("/recommend")
def recommend():
    movie = request.args.get('movie')  # get movie name from the URL

    movie_cards, cast_cards, result, keyvalue, img_path, genre, vote_count, rd, runtime = objectContentBased.content_based_function(
        movie)

    collaborativeCards = objectCollaborativeBased.item_based_function(
        movie)

    return render_template('recommendation.html', movie=movie, cards=movie_cards, CollaborativeCards=collaborativeCards,
                           cast=cast_cards, result=result, keyvalue=keyvalue, img_path=img_path, genres=genre,
                           release_date=rd, runtime=runtime)


@app.route("/recommenduserId")
def recommenduserId():
    Id = request.args.get('userId')
    userId = int(Id)

    user_collaborativeCard = objectCollaborativeBased.user_based_function(
        userId)

    return render_template('user_recommendation.html', UserCollaborativeCards=user_collaborativeCard)


if __name__ == '__main__':
    app.run(debug=True)
