from flask import Flask, render_template
from datetime import datetime
import view

def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", view_func=view.home_page)
    app.add_url_rule("/movies", view_func=view.movies_page)
    app.config.from_object("settings")
    #app.config["DEBUG"] = True
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)