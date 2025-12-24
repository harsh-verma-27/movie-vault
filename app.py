from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")
API_KEY = os.getenv("OMDB_API_KEY")

def get_db_connection():
    conn = sqlite3.connect("vault.db")
    conn.row_factory = sqlite3.Row
    return conn

'''Creates table if not there already'''
def init_db():
    conn = get_db_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS movies (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 year TEXT,
                 poster TEXT
                 )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods = ["GET"])
def home():
    search_query = request.args.get('search')
    movie_list = []
    if search_query:
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&s={search_query}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("Response") == "True":
                movie_list = data.get("Search")
        except request.exceptions.RequestException as e:
            flash("Movie service is currently unreachable. Please try again later.", "warning")
            print(f"Connection Error: {e}") # This shows in your terminal for debugging

    return render_template("index.html", movie = movie_list)

@app.route("/save", methods = ["POST"])
def save_movie():
    title = request.form["title"]
    year = request.form["year"]
    poster = request.form["poster"]
    search_word = request.form["curr_search"]
    conn = get_db_connection()
    exists = conn.execute("SELECT * FROM movies WHERE title = ? AND year = ?", (title, year)).fetchone()
    if exists:
        flash(f"'{title}' is already in your vault!", "warning")
    else:
        conn.execute("INSERT INTO movies (title, year, poster) VALUES (?, ?, ?)",
                 (title, year, poster))
        conn.commit()
        flash(f"Added '{title}' to your vault!", "success")
    conn.close()
    return redirect(url_for("home", search=search_word))

@app.route("/vault")
def view_vault():
    prev_search = request.args.get('last_search')
    conn = get_db_connection()
    movies = conn.execute("SELECT * FROM movies").fetchall()
    conn.close()
    return render_template("vault.html", movies = movies, back_word = prev_search)

@app.route("/delete/<int:movie_id>", methods = ["POST"])
def delete_movie(movie_id):
    prev_search = request.args.get('remember')
    conn = get_db_connection()
    conn.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_vault", last_search = prev_search))

@app.route("/delete_all", methods = ["POST"])
def delete_all():
    prev_search = request.args.get('remember')
    conn = get_db_connection()
    conn.execute("DELETE FROM movies")
    conn.commit()
    conn.close()
    return redirect(url_for("view_vault", last_search=prev_search))

@app.route("/details/<movie_id>", methods = ["GET"])
def details(movie_id):
    query = request.args.get('search_term')
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&i={movie_id}"
    response = requests.get(url)
    data = response.json()
    return render_template("details.html", movie=data, back_to = query)

if __name__ == "__main__":
    app.run(debug=True)
