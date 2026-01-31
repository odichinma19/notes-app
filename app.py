from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes").fetchall()
    conn.close()
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db()
        conn.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, id))
        conn.commit()
        conn.close()

        return redirect("/")

    note = conn.execute("SELECT * FROM notes WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", note=note)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    app.run(debug=True)
