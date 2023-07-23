from flask import Flask, render_template, request, redirect
from random import randint
random_id = randint(1,24)
import sqlite3

app = Flask(__name__)



def get_random_data():
    conn = sqlite3.connect("Database/final.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Movie ORDER BY RANDOM() LIMIT 5")  # Change 'your_table' to your actual table name
    data = cursor.fetchall()
    conn.close()
    return data

# This is the route for the home page
@app.route('/')
def home():
    random_data = get_random_data()
    return render_template('home.html', data=random_data)



# This is the route for the about page


@app.route('/about')
def about():
    return render_template("about.html", title="About")
  


@app.route('/contact')
def contact():
    return render_template("contact.html", title="Contact")

@app.route('/movies', methods=['POST'])
def add_movies():
    name = request.form['name']
    review = request.form['review']
    rating = request.form['rating']
    conn = sqlite3.connect('Database/Final.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Review (name, rating, review) VALUES (?, ?, ?)', (name, rating, review,))
    conn.commit()
    return redirect("http://127.0.0.1:5000/movies")

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