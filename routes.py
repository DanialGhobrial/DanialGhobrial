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
def movies():
    conn = sqlite3.connect('Database/Final.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Movie')
    movies = cur.fetchall()
    return render_template('movies.html', movies=movies)

if __name__ == "__main__":
    app.run(debug=True)
