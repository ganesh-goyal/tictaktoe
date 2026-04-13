from flask import Flask, request, jsonify

app = Flask(__name__)

board = [""] * 9

@app.route("/")
def home():
    return "TicTacToe DevSecOps App Running"

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    pos = data.get("position")
    player = data.get("player")

    if board[pos] == "":
        board[pos] = player
        return jsonify(board)
    else:
        return "Invalid move", 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)