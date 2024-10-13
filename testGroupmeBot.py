from flask import Flask, request, jsonify
# NFL Import
from espn_api.football import League
import requests
import config

app = Flask(__name__)

# Returns team that beats its opponent by the smallest margin of victory for week 14
def week14_weekly(league):
    pass

# Returns team with a starter closest to 21 points without going over for week 13
def week13_weekly(league):
    pass

# Returns team with the starting WR with the most receptions for week 12
def week12_weekly(league):
    pass

# Returns team that loses with the highest score for week 11
def week11_weekly(league):
    pass

# Returns team that wins with the bigest points of margin of victory for week 10
def week10_weekly(league):
    pass

# Returns team closest to their projected point total (over OR under) for week 9
def week9_weekly(league):
    pass

# Returns team with highest scoring starter on the bench for week 8
def week8_weekly(league):
    pass

# Returns team with the most offensive touchdowns scored with their starters for week 7
def week7_weekly(league):
    pass

# Returns team with most points over their weekly projection with their starters for week 6
def week6_weekly(league):
    pass

# Returns team with any starter closest to 30 points (over OR under) for week 5
def week5_weekly(league):
    week_number = 5
    target = 30
    target_player = None
    player_team = None
    difference = 500

    box_scores = league.box_scores(week = week_number)

    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            difference_temp = abs(player.points - target)
            if difference_temp < difference:
                difference = difference_temp
                target_player = player

                if player in box_score.home_lineup:
                    player_team = box_score.home_team.team_name
                else:
                    player_team = box_score.away_team.team_name

    if target_player:
        return {
            'team_name': player_team,
            'player_name': target_player.name,
            'player_points': target_player.points,
            'difference': f"{difference:.2f}"

        }
    else:
        return None

# Returns team with the starting RB with the most rushing yards for week 4
def week4_weekly(league):
    week_number = 4
    most_rush_yards = -1
    top_rb = None
    top_rb_team = None

    box_scores = league.box_scores(week=week_number)

    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.position == "RB":
                if 'breakdown' in player.stats[4] and 'rushingYards' in player.stats[4]['breakdown']:
                        rushing_yards = player.stats[4]['breakdown']['rushingYards']
                else:
                    rushing_yards = 0  # Fallback if rushingYards doesn't exist
                
                if rushing_yards > most_rush_yards:
                    most_rush_yards = rushing_yards
                    top_rb = player
                
                    if player in box_score.home_lineup:
                        top_player_team = box_score.home_team.team_name
                    else:
                        top_player_team = box_score.away_team.team_name

    if top_rb:
        return {
            'player_name': top_rb.name,
            'player_rushing_yards': most_rush_yards,
            'team_name': top_player_team

        }
    else:
        return None
            



# Returns team with most total points from their bench for week 3
def week3_weekly(league):
    week_number = 3

    max_bench_points = -1
    top_team = None

    box_scores = league.box_scores(week=week_number)

    for box_score in box_scores:
        home_bench_points = sum(player.points for player in box_score.home_lineup if player.lineupSlot == "BE")
        away_bench_points = sum(player.points for player in box_score.away_lineup if player.lineupSlot == "BE")

        if home_bench_points > max_bench_points:
            max_bench_points = home_bench_points
            top_team = box_score.home_team

        if away_bench_points > max_bench_points:
            max_bench_points = away_bench_points
            top_team = box_score.away_team

    if top_team:
        return {
            'team_name': top_team.team_name,
            'bench_points': f"{max_bench_points:.2f}"
        }
    else:
        return None

# this doesn't work as intended
# Returns team with starter QB who threw the longest pass (touchdown or not) for week 2
def week2_weekly(league):
    week_number = 1 # change this to 2
    longest_pass = -1
    top_qb = None
    top_qb_team = None
    stats = []
    dummy_response = 'this doesn\'t work right now, try another command' 

    box_scores = league.box_scores(week=week_number)
    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            # Check if the player is a QB
            if player.position == 'QB':
                # Access player's stats for passing data
                stats.append(player)
                stats.append(player.stats)

    # Return the top QB information
    return dummy_response


# Returns team with starter who scored the most points for week 1
def week1_weekly(league):
    week_number = 1
    
    max_points = -1
    top_player = None
    top_player_team = None

    box_scores = league.box_scores(week=week_number)
    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.points > max_points:
                max_points = player.points
                top_player = player

                if player in box_score.home_lineup:
                    top_player_team = box_score.home_team.team_name
                else:
                    top_player_team = box_score.away_team.team_name

    if top_player:
        return {
            'player_name': top_player.name,
            'player_points': top_player.points,
            'player_team': top_player_team
        }
    else:
        return None

# this method is for testing
def fetch_fantasy_data():
    try:
        # Initialize the league object
        league = League(league_id=config.ESPN_LEAGUE_ID, year=config.ESPN_SEASON_YEAR)
        
        # Extract relevant team data and format it into a JSON-serializable formatd
        team_data = []
        # for team in league.teams:
        #     team_info = {
        #         'team_name': team.team_name
        #     }
        #     team_data.append(team_info)
        
        top_rushing_yards = 0
        top_player = None
        week_number = 4
        box_scores = league.box_scores(week=week_number)
        for box_score in box_scores:
            for player in box_score.home_lineup + box_score.away_lineup:
                if 'breakdown' in player.stats[4] and 'rushingYards' in player.stats[4]['breakdown']:
                    rushing_yards = player.stats[4]['breakdown']['rushingYards']
                else:
                    rushing_yards = 0  # Fallback if rushingYards doesn't exist
                
                if rushing_yards > top_rushing_yards:
                    top_rushing_yards = rushing_yards
                    top_player = player
                
                player_info = {
                    'player_name': player,
                    'rush yards': top_rushing_yards
                }
                team_data.append(player_info)
            
        return player_info
    except Exception as e:
        print(f"Error fetching fantasy data: {e}")
        return None


@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    league = League(league_id=config.ESPN_LEAGUE_ID, year=config.ESPN_SEASON_YEAR)

    # Ignore messages from the bot itself
    if data['sender_type'] == 'bot':
        return "OK", 200

    # This is the message from the chat
    message = data['text'].lower()
    
    if not message.startswith('!'):
            return "OK", 200

    if '!hello' in message:
        response_message = "Hi there! How can I assist you today?"
    elif '!fantasy' in message:
        fantasy_data = fetch_fantasy_data()
        if fantasy_data:
            # You can customize the response based on the data you retrieved
            response_message = f"Fantasy league data: {fantasy_data}"
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly1' in message:
        fantasy_data = week1_weekly(league)
        player_name = fantasy_data.get('player_name')
        player_points = fantasy_data.get('player_points')
        player_team = fantasy_data.get('player_team')
        if fantasy_data:
            # You can customize the response based on the data you retrieved
            response_message = f"Winner of Weekly 1: Get Schwifty - Team with the single highest scoring starter: \n\n{player_team} ({player_name} {player_points})" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly2' in message:
        fantasy_data = week2_weekly(league)
        # player_name = fantasy_data.get('qb_name')
        if fantasy_data:
            # You can customize the response based on the data you retrieved
            response_message = f"{fantasy_data}." 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly3' in message:
        fantasy_data = week3_weekly(league)
        team_name = fantasy_data.get('team_name')
        total_points = fantasy_data.get('bench_points')
        # player_name = fantasy_data.get('qb_name')
        if fantasy_data:
            # You can customize the response based on the data you retrieved
            response_message = f"Winner of Weekly 3: Bench Warmer - Team with the most total points from their bench: \n\n{team_name} ({total_points} bench points)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly4' in message:
        fantasy_data = week4_weekly(league)
        team_name = fantasy_data.get('team_name')
        player_name = fantasy_data.get('player_name')
        player_rushing_yards = fantasy_data.get('player_rushing_yards')
        if fantasy_data:
            response_message = f"Winner of Weekly 4: Run Forrest Run! - Team with the starting RB with the most rushing yards: \n\n{team_name} ({player_name} {player_rushing_yards} rush yards)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly5' in message:
        fantasy_data = week5_weekly(league)
        team_name = fantasy_data.get('team_name')
        player_name = fantasy_data.get('player_name')
        player_points = fantasy_data.get('player_points')
        difference = fantasy_data.get('difference')
        if fantasy_data:
            response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly6' in message:
        fantasy_data = week6_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly7' in message:
        fantasy_data = week7_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly8' in message:
        fantasy_data = week8_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly9' in message:
        fantasy_data = week9_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly10' in message:
        fantasy_data = week10_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly11' in message:
        fantasy_data = week11_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly12' in message:
        fantasy_data = week12_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly13' in message:
        fantasy_data = week13_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly14' in message:
        fantasy_data = week14_weekly(league)
        if fantasy_data:
            response_message = f"method not ready yet"
            # response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    else:
        response_message = "what you say bruh?"
    
    send_message(response_message)
    return jsonify({"status": "OK", "response": response_message}), 200

  
  
def send_message(msg):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id': config.BOT_ID,
        'text': msg
    }
    requests.post(url, json=data)

if __name__ == '__main__':
    app.run(debug=True)