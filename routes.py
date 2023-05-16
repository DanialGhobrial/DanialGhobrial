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


@app.route('/movies/<int:id>')
def movie(id):
    conn = sqlite3.connect('Database/Final.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Movie WHERE id=?',(id,))
    Raiting = cur.fetchone()
    cur.execute('SELECT * FROM Raiting WHERE id=?',(movie[4],))
    Movie = cur.fetchone()
    cur.execute('SELECT * FROM Movie WHERE id=?',(movie[3],))
    review = cur.fetchone()
    cur.execute('SELECT * FROM review WHERE id=?',(movie[3],))
    return render_template('movies.html', movie=movie,rating=rating,review=review)

if __name__ == "__main__":
    app.run(debug=True)
