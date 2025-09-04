from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- Game Logic ---
board = [[" - " for _ in range(3)] for _ in range(3)]
current_player = "X"
game_won = ""

# Place a move
def place_move(player, row, col):
    if board[row][col] != " - ":
        return False
    board[row][col] = player
    return True

# Check for a win
def check_win(player):
    # Rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Check for a draw
def check_draw():
    return all(cell != " - " for row in board for cell in row)

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


# --- Flask Routes ---
@app.route('/')
def home():
    return render_template("index.html", board=board, game_won=game_won)

@app.route('/reset')
def reset():
    global board, current_player, game_won
    board = [[" - " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_won = ""
    return redirect(url_for("home"))

@app.route('/move/<int:row>/<int:col>')
def move(row, col):
    global current_player
    global game_won

    if board[row][col] == " - " and game_won == "":
        place_move(current_player, row, col)
        current_player = "O" if current_player == "X" else "X"
    
    if check_win("X"):
        game_won="X"
    elif check_win("O"):
        game_won="O"
    elif check_draw():
        game_won="draw"
    
    return redirect(url_for("home"))#render_template("index.html", board=board)

if __name__ == '__main__':
    app.run(debug=True)
