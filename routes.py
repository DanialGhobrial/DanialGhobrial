from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# This is the route for the home page


@app.route('/')
def home():
    return render_template("home.html", title="Home")

# This is the route for the about page


@app.route('/about')
def about():
    return render_template("about.html", title="About")


@app.route('/contact')
def contact():
    return render_template("contact.html", title="Contact")


@app.route('/movies')
def movies():
    conn = sqlite3.connect('Database/Final.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Movie')
    movies = cur.fetchall()
    return render_template('movies.html', movies=movies)


@app.route('/movie_detail/<int:id>')
def movies_detail(id):
    conn = sqlite3.connect('Database/final.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Movie WHERE id=?', (id,))
    movie = cur.fetchone()
    cur.execute('SELECT * FROM Movie WHERE id=?', (movie[1],))
    genre = cur.fetchone()
    cur.execute('SELECT * FROM Movie WHERE id=?', (movie[3],))
    director = cur.fetchone()
    cur.execute('SELECT * FROM Movie WHERE id=?', (movie[4],))
    image = cur.fetchone()
    cur.execute('SELECT * FROM movie WHERE id=?', (movie[5],))
    return render_template('movie_detail.html', movie=movie, genre=genre, director=director, image=image)


if __name__ == "__main__":
    app.run(debug=True)
