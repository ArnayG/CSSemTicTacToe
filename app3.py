from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_data(school_type=None):
    rows = []
    try:
        with sqlite3.connect("Track.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            if school_type:
                cur.execute("SELECT school_name, school_type FROM school WHERE school_type = ?", (school_type,))
            else:
                cur.execute("SELECT school_name, school_type FROM school")
            rows = cur.fetchall()
    except sqlite3.Error as e:
        print("Database error:", e)
    return rows

@app.route("/")
def index():
    school_type = request.args.get('school_type')
    data = get_data(school_type)
    return render_template("index3.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)