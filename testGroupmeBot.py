from flask import Flask, request
# NFL Import
from espn_api.football import League
import requests

app = Flask(__name__)

BOT_ID = 'asdf'
ESPN_LEAGUE_ID = 1234  # Replace with your ESPN league ID
ESPN_SEASON_YEAR = 2024

def fetch_fantasy_data():
    try:
        # Initialize the league object
        league = League(league_id=1234, year=2024)
        
        # Extract relevant team data and format it into a JSON-serializable formatd
        team_data = []
        for team in league.teams:
            team_info = {
                'team_name': team.team_name
            }
            team_data.append(team_info)
        
        return team_data
    except Exception as e:
        print(f"Error fetching fantasy data: {e}")
        return None


@app.route('/', methods=['POST'])
def webhook():
    data = request.json

    # Ignore messages from the bot itself
    if data['sender_type'] == 'bot':
        return "OK", 200

    # Sample response: echo the message back
    message = data['text'].lower()
    
    if 'hello' in message:
        response_message = "Hi there! How can I assist you today?"
    elif 'fantasy' in message:
        fantasy_data = fetch_fantasy_data()
        if fantasy_data:
            # You can customize the response based on the data you retrieved
            response_message = f"Fantasy league data: {fantasy_data}"
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    else:
        response_message = "what you say bruh?"
    
    send_message(response_message)
    return "OK", 200

  
  
def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id': BOT_ID,
        'text': msg
    }
    requests.post(url, json=data)

if __name__ == '__main__':
    app.run(debug=True)