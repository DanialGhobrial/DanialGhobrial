from flask import Flask, render_template, request, redirect, url_for
from math import ceil
import sqlite3

app = Flask(__name__)


# Function to get random data from the 'Movie' table
def get_random_data():
    with sqlite3.connect("Database/Final.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Movie ORDER BY RANDOM() LIMIT 4")
        data = cursor.fetchall()
    return data


# Route for the home page
@app.route('/')
def home():
    random_data = get_random_data()
    return render_template('home.html', data=random_data)


# Route for the about page
@app.route('/about')
def about():
    return render_template("about.html", title="About")


# Route for the contact page
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
    with sqlite3.connect('Database/Final.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Review (name, rating, review, movie_id) VALUES (?, ?, ?, ?)',
                       (name, rating, review, movie_id))
        conn.commit()
    return redirect(url_for('movies_detail', id=movie_id))
# Redirect back to the movie details page because it is more logical for the user to see their review after they write it


# Route to display a list of movies and handle the search form
@app.route('/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        # Handle the form submission here (if needed)
        pass

    # Retrieve genres from the database
    with sqlite3.connect('Database/Final.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT genre FROM Movie')
        genres_list = [genre for row in cur.fetchall() for genre in row[0].split(',')]
        genres = list(set(genres_list))

    search_query = request.args.get('search_query')
    genre_filter = request.args.get('genre_filter')  # Get the selected genre

    # Construct the SQL query based on search_query and genre_filter
    query = 'SELECT * FROM Movie'
    params = []

    if search_query or genre_filter:
        query += ' WHERE'

        if search_query:
            query += ' (title LIKE ?)'
            params.extend([f'%{search_query}%'])

        if genre_filter:
            if search_query:
                query += ' AND'
            query += ' genre LIKE ?'
            params.append(f'%{genre_filter}%')

    query += ' ORDER BY title'  # this is so that it looks better for the end user consideration

    # Execute the constructed query
    with sqlite3.connect('Database/Final.db') as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        movies = cur.fetchall()

    # Pagination logic
    items_per_page = 28  # 28 pages because its what looked the most visually pleasing
    num_pages = ceil(len(movies) / items_per_page)
    page = int(request.args.get('page', 1))
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    movies_to_display = movies[start_idx:end_idx]

    return render_template('movies.html', movies=movies_to_display, genres=genres, page=page, num_pages=num_pages)


# Route for the contact page and to connect the contact form
@app.route('/contact', methods=['POST'])
def add_contact():
    conn = sqlite3.connect('Database/final.db')
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    conn = sqlite3.connect('Database/Final.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Contact (name, email, subject, message) VALUES (?, ?, ?, ?)', (name, email, subject, message))
    conn.commit()
    return redirect("http://127.0.0.1:5000/contact")
# redirect back to the contact page incase they wanted to contact again.


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


# Custom error handling for page not found errors for the end user consideration
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error='Page not found'), 404


# Custom error handling for 500 (Internal Server Error) error for the end user consideration
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html', error='Internal server error'), 500


# Custom error handling for other unexpected errors for the end user consideration
@app.errorhandler(Exception)
def unexpected_error(error):
    return render_template('error.html', error='Something went wrong'), 500


if __name__ == "__main__":
    app.run(debug=True)
