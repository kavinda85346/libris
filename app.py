from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_title TEXT NOT NULL,
            book_isbn TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home - List books
@app.route('/')
def index():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

# Add book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        author = request.form['author']
        year = request.form['year']
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (book_title, book_isbn, author, year) VALUES (?, ?, ?, ?)",
                       (title, isbn, author, year))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_book.html')

# Edit book
@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
    book = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        author = request.form['author']
        year = request.form['year']

        cursor.execute("UPDATE books SET book_title=?, book_isbn=?, author=?, year=? WHERE book_id=?",
                       (title, isbn, author, year, book_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit_book.html', book=book)

# Delete book
@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
