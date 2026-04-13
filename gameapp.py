from flask import Flask, request, jsonify, session
import os
import sqlite3
import logging

app = Flask(__name__)

# 🚨 Hardcoded secret (SAST issue)
app.secret_key = "super-secret-key"

# 🚨 Insecure logging
logging.basicConfig(filename="app.log", level=logging.DEBUG)

# In-memory board
board = [""] * 9


# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return "TicTacToe DevSecOps App Running"


# -----------------------------
# START GAME
# -----------------------------
@app.route("/start", methods=["POST"])
def start_game():
    username = request.json.get("username")

    # 🚨 No validation
    session["user"] = username

    logging.info(f"User {username} started a game")

    return {"message": "Game started", "user": username}


# -----------------------------
# MAKE MOVE
# -----------------------------
@app.route("/move", methods=["POST"])
def move():
    data = request.json

    pos = data.get("position")
    player = data.get("player")

    # 🚨 No input validation
    if board[pos] == "":
        board[pos] = player
        return jsonify(board)
    else:
        return "Invalid move", 400


# -----------------------------
# RESET GAME
# -----------------------------
@app.route("/reset", methods=["POST"])
def reset():
    global board
    board = [""] * 9
    return {"message": "Board reset"}


# -----------------------------
# SAVE GAME (DB)
# -----------------------------
@app.route("/save", methods=["POST"])
def save_game():
    user = session.get("user", "guest")

    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    # 🚨 SQL Injection vulnerability
    query = f"INSERT INTO games (user, state) VALUES ('{user}', '{str(board)}')"
    cursor.execute(query)

    conn.commit()
    conn.close()

    return {"message": "Game saved"}


# -----------------------------
# LOAD GAME
# -----------------------------
@app.route("/load", methods=["GET"])
def load_game():
    user = request.args.get("user")

    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    # 🚨 SQL Injection
    query = f"SELECT state FROM games WHERE user='{user}'"
    cursor.execute(query)

    result = cursor.fetchone()
    conn.close()

    return {"data": result}


# -----------------------------
# FILE READ (LFI)
# -----------------------------
@app.route("/readfile", methods=["GET"])
def read_file():
    filename = request.args.get("file")

    # 🚨 Path traversal
    with open(filename, "r") as f:
        data = f.read()

    return {"content": data}


# -----------------------------
# COMMAND EXECUTION (CRITICAL)
# -----------------------------
@app.route("/run", methods=["GET"])
def run_command():
    cmd = request.args.get("cmd")

    # 🚨 Command injection
    output = os.popen(cmd).read()

    return {"output": output}


# -----------------------------
# DEBUG ROUTE
# -----------------------------
@app.route("/debug", methods=["GET"])
def debug():
    return {
        "env": dict(os.environ),
        "cwd": os.getcwd()
    }


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    # 🚨 Debug mode enabled
    app.run(host="0.0.0.0", port=5000, debug=True)