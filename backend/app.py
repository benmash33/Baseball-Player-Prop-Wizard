from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key
CORS(app)

class PlayerPitcherForm(FlaskForm):
    player_name = StringField('Player Name', validators=[DataRequired()])
    pitcher_name = StringField('Pitcher Name', validators=[DataRequired()])

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/submit-names', methods=['POST'])
def submit_names():
    form = PlayerPitcherForm(meta={'csrf': False})  # Disable CSRF for API use
    if form.validate_on_submit():
        player_name = form.player_name.data
        pitcher_name = form.pitcher_name.data
        # Process the data as needed
        return jsonify({
            "message": "Names received",
            "player_name": player_name,
            "pitcher_name": pitcher_name
        }), 200
    return jsonify({"errors": form.errors}), 400

if __name__ == '__main__':
    app.run(debug=True)