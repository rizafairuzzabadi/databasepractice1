from flask import Flask, render_template
from datetime import datetime

def home_page():
    today=datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def movies_page():
    return render_template("movies.html")