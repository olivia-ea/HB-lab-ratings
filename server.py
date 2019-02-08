"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/register', methods=["GET"])
def register_form():

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():

    email = request.form['email']
    password = request.form['password']
    age = int(request.form['age'])
    zipcode = request.form['zipcode']

    check_email = User.query.filter(User.email == email).first()

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    if check_email:
        flash(f"User {email} already registered")
        return redirect('/login')
    else:
        db.session.add(new_user)
        db.session.commit()
        flash(f"User {email} added")
        return redirect('/')

@app.route('/login', methods=['GET'])
def login_form():

    return render_template('login_form.html')

@app.route('/login', methods=['POST'])
def login_process():

    email = request.form['email']
    password = request.form['password']

    check_password = User.query.filter(User.password == password).first()

    if check_password:
        session['email'] = email
        flash(f'Logged in as {email}')
        return redirect('/')
    else:
        flash(f'Wrong password')
        return redirect('/login')

@app.route('/logout')
def logout():

    if session['email']:
        logout_message = session.pop('email')
        flash(f'Logged out {logout_message}')

    
    return redirect("/")


@app.route('/users')
def user_list():
    users = User.query.all()

    return render_template('user_list.html', users=users)

# @app.route("/users/<int:user_id>")
# def user_detail(user_id):



# @app.route("/movies")
# def movie_list():
#     """Show list of movies."""

#     return render_template("movie_list.html", movies=movies)


# @app.route("/movies/<int:movie_id>", methods=['GET'])
# def movie_detail(movie_id):
#     """Show info about movie.

#     If a user is logged in, let them add/edit a rating.
#     """


#     return render_template("movie.html",
#                            movie=movie,
#                            user_rating=user_rating)


# @app.route("/movies/<int:movie_id>", methods=['POST'])
# def movie_detail_process(movie_id):
#     """Add/edit a rating."""

#     # Get form variables


#     return redirect(f"/movies/{movie_id}")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
