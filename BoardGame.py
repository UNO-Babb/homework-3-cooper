#Example Flask App for a hexaganal tile game
#Logic is in this python file

# Jungle Journey app using FLask
from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Track the current player and player details
current_player = 1
players = {
    1: {"color": "green", "score": 0},
    2: {"color": "blue", "score": 0}
}
tile_positions = {}  # key: (row, col), value: {'player': 1 or 2, 'effect': str}

# Special tiles with effects
effects = {
    (2, 3): "Treasure",
    (4, 5): "Thief",
    (1, 1): "Den",
    (2,4): "Treasure",
    (5,2): "Thief",
    (3,3): "Den",
    (1,4): "Treasure",
    (3,4): "Treasure"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_tile', methods=['POST'])
def add_tile():
    global current_player
    data = request.get_json()
    row = data['row']
    col = data['col']

    if (row, col) in tile_positions:
        return jsonify(success=False, message="Tile already occupied")

    # Lock in current player before switching
    this_player = current_player
    color = players[this_player]['color']
    tile_effect = effects.get((row, col))

    if tile_effect == "Treasure":
        players[this_player]['score'] += 3
        message = f"Player {this_player} found Treasure! +3 points"
    elif tile_effect == "Thief":
        players[this_player]['score'] -= 2
        message = f"Player {this_player} encountered a Thief -2 points"
    elif tile_effect == "Den":
        message = f"Player {this_player} is resting in a Den. No score change."
    else:
        message = f"Player {this_player} placed a tile."

    tile_positions[(row, col)] = {
        "player": this_player,
        "effect": tile_effect
    }

    response = {
        "success": True,
        "color": color,
        "message": message,
        "tile": {"row": row, "col": col},
        "player": this_player,
        "scores": {
            1: players[1]['score'],
            2: players[2]['score']
        },
        "next_player": 2 if this_player == 1 else 1
    }

    # Switch turn
    current_player = response["next_player"]

    return jsonify(response)

@app.route('/state')
def game_state():
    return jsonify({
        "tiles": tile_positions,
        "scores": {
            1: players[1]['score'],
            2: players[2]['score']
        },
        "current_player": current_player
    })

if __name__ == "__main__":
    app.run(debug=True)
