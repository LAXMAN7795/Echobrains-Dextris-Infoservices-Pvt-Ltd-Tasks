from flask import Flask, request, jsonify
import random
import database

app = Flask(__name__)

# Create table on startup
database.create_table()

@app.route("/start-game", methods=["POST"])
def start_game():
    data = request.json
    p1 = data["player1"]
    p2 = data["player2"]
    p1_symbol = data["symbol"]  # X or O

    p2_symbol = "O" if p1_symbol == "X" else "X"

    first_player = random.choice([p1, p2])

    return jsonify({
        "player1": p1,
        "player2": p2,
        "player1_symbol": p1_symbol,
        "player2_symbol": p2_symbol,
        "first_player": first_player
    })

@app.route("/save-result", methods=["POST"])
def save_result():
    data = request.json

    database.save_result(
        data["player1"],
        data["player2"],
        data["player1_symbol"],
        data["player2_symbol"],
        data["first_player"],
        data["winner"]
    )

    return jsonify({"message": "Result saved successfully"})

if __name__ == "__main__":
    app.run(debug=True)