from flask import Flask,render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html",title="Home")


@app.route('/about')
def about():
    return render_template("about.html",title="About")


@app.route('/contact')
def contact():
    return render_template("contact.html",title="Contact")


@app.route('/movies')
def movie():
    conn = sqlite3.connect('Database/Final.db')
    cur = conn.cursor()
    movie = cur.fetchone()
    cur.execute('SELECT * FROM Movie WHERE id=?',(movie[1],))
    genre = cur.fetchone()
    cur.execute('SELECT * FROM Movie WHERE id=?',(movie[3],))
    director = cur.fetchone()
    cur.execute('SELECT * FROM Movie WHERE id=?',(movie[4],))
    return render_template('movies.html', movie=movie,genre=genre,director=director)

if __name__ == "__main__":
    app.run(debug=True)
