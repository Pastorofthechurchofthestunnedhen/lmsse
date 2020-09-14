from datetime import timedelta
from books import Books
from flask import Flask, flash, redirect, url_for, render_template, request, session
from user import User
from database import Database

Database.initialise(user='postgres',
                    password='8408905902',
                    database='libraryexample',
                    host='localhost')
app = Flask(__name__)
app.secret_key = "lmsprojse1minipres"
app.permanent_session_lifetime = timedelta(minutes=4)


@app.route('/')
@app.route('/home')
def hello_world():
    return render_template("home.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        userc = User(first_name=request.form["firstname"],
                     last_name=request.form["lastname"],
                     password=request.form["psw"],
                     email=request.form["email"],
                     phone_number=request.form["pnumber"],
                     id=None)
        userc.new_user()
        userc.id = userc.assignid(userc.email)
        session["user"] = userc.id
        flash("login successful")
        return redirect(url_for("user"))
    else:
        return render_template("login.html")
@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":

        name = request.form["firstname"]
        isbn = request.form["lastname"]
        author = request.form["psw"]
        language = request.form["email"]
        publisher = request.form["pnumber"]
        results = Books.search(name, isbn, author, language, publisher)
        return redirect(url_for("results", result=results))
    else:
        return render_template("search.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    if "user" in session:
        userid = session["user"]

        return
    else:
        return redirect(url_for("login"))




@app.route("/results")
def results(result):
    return render_template(results.html)


@app.route("/logout")
def logout():
    flash("you have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(port=5000, debug=True)
