from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import r
import uuid

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Necesario para flash messages

# Ruta principal
@app.route("/")
def index():
    books = []
    for key in r.keys("book:*"):
        books.append(r.hgetall(key))
    return render_template("index.html", books=books)

# Agregar libro
@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_id = str(uuid.uuid4())
        title = request.form["title"]
        author = request.form["author"]

        r.hset(f"book:{book_id}", {
            "id": book_id,
            "title": title,
            "author": author
        })
        flash("Libro agregado correctamente")
        return redirect(url_for("index"))
    return render_template("add_book.html")

# Editar libro
@app.route("/edit/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book_key = f"book:{book_id}"
    book = r.hgetall(book_key)

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        r.hset(book_key, {
            "id": book_id,
            "title": title,
            "author": author
        })
        flash("Libro actualizado correctamente")
        return redirect(url_for("index"))

    return render_template("edit_book.html", book=book)

# Eliminar libro
@app.route("/delete/<book_id>")
def delete_book(book_id):
    r.delete(f"book:{book_id}")
    flash("Libro eliminado correctamente")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
