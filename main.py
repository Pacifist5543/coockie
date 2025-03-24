from flask import Flask, render_template, request, make_response, session, redirect
import sqlite3
import secrets
from user import User, create_user_table
from post import Post, create_post_table


class Movie:
    def __init__(
        self,
        id,
        title,
        year,
        genres,
        country,
        description,
        duration,
        rating,
        age_rating,
        poster,
    ):
        self.id = id
        self.title = title
        self.year = year
        self.genres = genres
        self.country = country
        self.description = description
        self.duration = duration
        self.rating = rating
        self.age_rating = age_rating
        self.poster = poster


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)


db_name = "./films.db"


def get_films_lists(page=1, offset=25, limit=25):
    con = sqlite3.connect(db_name)

    SQL = """

        SELECT * FROM movie
        LIMIT ?
        OFFSET ?
    """

    q = con.execute(SQL, [limit, (offset * (page - 1))])
    data = q.fetchall()
    return [Movie(*row) for row in data]


def get_films_by_search(search):
    con = sqlite3.connect(db_name)

    SQL = f"""

        SELECT * FROM movie where title like '%{search}%' or country like '%{search}%' or genres like '%{search}%'
    """

    q = con.execute(SQL)
    data = q.fetchall()
    return [Movie(*row) for row in data]


def get_film(film_id):
    con = sqlite3.connect(db_name)

    SQL = """

        SELECT * FROM movie
        where id = ?
    """

    q = con.execute(SQL, [film_id])
    data = q.fetchone()
    return Movie(*data)


@app.route("/")
@app.route("/pages/<int:page>")
def index_page(page=1):
    films = get_films_lists(page)

    
    username  =  session.get("username") 

    return render_template("index.html", films=films, page=page, username=username)


@app.route("/films/<int:film_id>")
def film_page(film_id):
    film = get_film(film_id)
    return render_template("film.html", film=film)


@app.route("/search", methods=["POST"])
def search_page():
    search = request.form.get("search")
    films = get_films_by_search(search)
    return render_template("search.html", films=films, search=search)


create_post_table()


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = user.get_user_by_username(username)
        pas_hash = user.hashed_password_hash(password)
        if not user:
            error = "Неправильный логин или пароль"

        if not user:
            error = "Неправильный логин или пароль"

        if error:
            return render_template("login.html", error=error)

        session["username"] = username
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        error = None

        user = User.get_users_by_username(username)
        if user:
            error = "Такой пользователь уже есть"

        if password != confirm_password:
            error = "Пароли не совпадают"

        if error:
            return render_template("register.html", error=error)

        User.creat(username, password)
        session["username"] = username
        return redirect("/")


@app.route("/logout")
def logout_page():
    username = session.get("username")
    if username:
        del session["username"]
    return redirect("/login")


@app.route("/profile")
def profile_page():
    return ""


app.run(host="0.0.0.0", port=8080, debug=True)
