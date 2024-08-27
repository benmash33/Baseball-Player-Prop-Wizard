from flask import Flask, jsonify
from flask_cors import CORS
from pybaseball import chadwick_register

app = Flask(__name__)
CORS(app)

@app.route('/api/mlb-players', methods=['GET'])
def mlb_players():
    try:
        # Get all players from the Chadwick Register
        all_players = chadwick_register()
        
        # Filter for active players (those with no 'final_game' date)
        active_players = all_players[all_players['final_game'].isna()]
        
        # Format the data
        formatted_players = [
            {
                "id": player['key_mlbam'],
                "name": f"{player['name_first']} {player['name_last']}",
            }
            for _, player in active_players.iterrows() if player['key_mlbam']
        ]
        
        return jsonify(formatted_players)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)