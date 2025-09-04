from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_data():
    rows = []
    try:
        with sqlite3.connect("Track.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT school_name, school_type FROM school")
            rows = cur.fetchall()
    except sqlite3.Error as e:
        print("Database error:", e)
    return rows

@app.route("/")
def index():
    data = get_data()
    return render_template("index3.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)