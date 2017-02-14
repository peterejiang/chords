from flask import Flask, render_template, request
import requests

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0")

