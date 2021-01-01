from flask import Flask, render_template
from datetime import datetime

import view
from database import Database
from movie import Movie


def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", view_func=view.home_page)
    app.add_url_rule("/movies", view_func=view.movies_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/new_movie", view_func=view.movie_add_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/movies/<int:movie_key>",
                     view_func=view.movie_page)
    db = Database()
    db.add_movie(Movie("Slaughterhouse-Five", year=1972))
    db.add_movie(Movie("The Shining"))
    app.config["db"] = db

    app.config.from_object("settings")
    #app.config["DEBUG"] = True
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080)
