from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Function to get random data from the 'Movie' table
def get_random_data():
    with sqlite3.connect("Database/Final.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Movie ORDER BY RANDOM() LIMIT 4")
        data = cursor.fetchall()
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

# This is the route for the contact page
@app.route('/contact')
def contact():
    return render_template("contact.html", title="Contact")

# Route to add a new review for a movie
@app.route('/add_review', methods=['POST'])
def add_movie_review():
    name = request.form['name']
    review = request.form['review']
    rating = request.form['rating']
    movie_id = request.form['movie_id']

    print(f"Name: {name}, Review: {review}, Rating: {rating}, Movie ID: {movie_id}")  # Debugging line

    with sqlite3.connect('Database/Final.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Review (name, rating, review, movie_id) VALUES (?, ?, ?, ?)',
                       (name, rating, review, movie_id))
        conn.commit()

    return redirect("/movie_detail/{}".format(movie_id))

# Route to display a list of movies and handle the search form
@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        # Handle the form submission for adding a review
        name = request.form['name']
        review = request.form['review']
        rating = request.form['rating']
        movie_id = request.form['movie_id']

        print(f"Name: {name}, Review: {review}, Rating: {rating}, Movie ID: {movie_id}")  # Debugging line

        with sqlite3.connect('Database/Final.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Review (name, rating, review, movie_id) VALUES (?, ?, ?, ?)',
                           (name, rating, review, movie_id))
            conn.commit()

        return redirect("/movie_detail/{}".format(movie_id))

    # Handle the search query
    query = request.args.get('query')
    if query:
        with sqlite3.connect('Database/Final.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM Movie WHERE title LIKE ? OR genre LIKE ? OR year LIKE ? OR director LIKE ?',
                        (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
            movies = cur.fetchall()
    else:
        with sqlite3.connect('Database/Final.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM Movie')
            movies = cur.fetchall()

    return render_template('movies.html', movies=movies)



# Route to display the details of a specific movie
@app.route('/movie_detail/<int:id>')
def movies_detail(id):
    with sqlite3.connect('Database/final.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM movie WHERE id=?', (id,))
        movie = cur.fetchone()

        cur.execute('SELECT * FROM movie WHERE id=?', (movie[3],))
        genre = cur.fetchone()

        cur.execute('SELECT * FROM movie WHERE id=?', (movie[4],))
        director = cur.fetchone()

        cur.execute('SELECT * FROM movie WHERE id=?', (movie[5],))
        image = cur.fetchone()

        cur.execute('SELECT * FROM Review WHERE movie_id=?', (id,))
        reviews = cur.fetchall()

    return render_template('movie_detail.html', movie=movie, genre=genre, director=director, image=image, reviews=reviews)


if __name__ == "__main__":
    app.run(debug=True)
