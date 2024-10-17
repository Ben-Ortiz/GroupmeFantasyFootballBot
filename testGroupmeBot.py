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
    week_number = 1
    top_teams = {}
    top_wrs = []
    all_wrs = {}
    max_receptions = 0

    box_scores = league.box_scores(week = week_number)

    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.slot_position == "WR" and player.slot_position != "BE":
                receptions = player.stats[week_number]['breakdown'].get('receivingReceptions', 0)
                all_wrs[player]  = receptions
    
    # max_receptions = max(all_wrs.values())
    max_receptions = 7
    top_wrs = [element for element, receptions in all_wrs.items() if receptions == max_receptions]

    # this to account for teams who have players with the same top receptions
    for box_score in box_scores:
        for player in top_wrs:
            if player in box_score.home_lineup:
                if box_score.home_team not in top_teams:
                    top_teams[box_score.home_team] = player
            elif player in box_score.away_lineup:
                if box_score.away_team not in top_teams:
                    top_teams[box_score.away_team] = player


    if top_wrs:
        return {
            "top_teams": top_teams,
            "max_receptions": max_receptions
        }
    else:
        return None
# Returns team that loses with the highest score for week 11
def week11_weekly(league):
    week_number = 11 # change this to 11
    top_loser = None
    top_loser_score = 0
    losing_teams = {}

    box_scores = league.box_scores(week=week_number)
    
    for box_score in box_scores:
        if box_score.home_score < box_score.away_score:
            losing_teams[box_score.home_team] = box_score.home_score
        else:
            losing_teams[box_score.away_team] = box_score.away_score

    top_loser = max(losing_teams, key=losing_teams.get)
    top_loser_score = losing_teams[top_loser]

    if top_loser:
        return {
            "top_loser" : top_loser.team_name,
            "top_loser_score" : top_loser_score
        }
    else:
        return None
    

# Returns team that wins with the bigest points of margin of victory for week 10
def week10_weekly(league):
    week_number = 10 # change this to 10
    winning_team = None
    winning_team_score = 0
    losing_team = None
    losing_team_score = 0
    difference = -1
    
    box_scores = league.box_scores(week=week_number)
    
    for box_score in box_scores:
        difference_both = abs(box_score.home_score - box_score.away_score)
        if difference_both > difference:
            difference = difference_both
            if box_score.home_score > box_score.away_score:
                winning_team = box_score.home_team
                winning_team_score = box_score.home_score
                losing_team = box_score.away_team
                losing_team_score = box_score.away_score
            else:
                winning_team = box_score.away_team
                winning_team_score = box_score.away_score
                losing_team = box_score.home_team
                losing_team_score = box_score.home_score
    
    return {
        "winning_team": winning_team.team_name,
        "winning_team_score": winning_team_score,
        "difference": difference,
        "losing_team": losing_team.team_name,
        "losing_team_score": losing_team_score
    }


# Returns team closest to their projected point total (over OR under) for week 9
def week9_weekly(league):
    week_number = 9 # change this to 9
    top_team = None
    difference = 500
    actual_score = 0
    projected_score = 0
    
    box_scores = league.box_scores(week = week_number)
    
    for box_score in box_scores:
        difference_home = abs(box_score.home_score - box_score.home_projected)
        if difference_home < difference:
            difference = difference_home
            top_team = box_score.home_team
            actual_score = box_score.home_score
            projected_score = box_score.home_projected
        
        difference_away = abs(box_score.away_score - box_score.away_projected)
        if difference_away < difference:
            difference = difference_away
            top_team = box_score.away_team
            actual_score = box_score.away_score
            projected_score = box_score.away_projected
        
    return {
        "top_team": top_team.team_name,
        "difference": difference,
        "actual_score": actual_score,
        "projected_score": projected_score
    }
    

# Returns team with highest scoring player on the bench for week 8
def week8_weekly(league):
    week_number = 1 # change this to 8
    top_team = None
    top_player = None
    top_player_points = 0
    box_scores = league.box_scores(week = week_number)
    
    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.slot_position == "BE":
                if player.points > top_player_points:
                    top_player_points = player.points
                    top_player = player
                    
                    if top_player in box_score.home_lineup:
                        top_team = box_score.home_team.team_name
                    else:
                        top_team = box_score.away_team.team_name        
    
    if top_team:
        return {
            'top_team': top_team,
            'top_player': top_player.name,
            'top_player_points': top_player_points
        }
    else:
        return None
                

# Returns team with the most offensive touchdowns scored with their starters for week 7
def week7_weekly(league):
    week_number = 7 #change this to 7
    top_team = None
    top_team_tds = 0

    rush_tds = 0
    receiving_tds = 0
    passing_tds = 0

    box_scores = league.box_scores(week=week_number)
    team_dict = {}
    for box_score in box_scores:
        
        total_tds_home = 0
        total_tds_away = 0

        for player in box_score.home_lineup:
            if player.slot_position != "D/ST" and player.slot_position != "BE":
                rush_tds = player.stats[week_number]['breakdown'].get('rushingTouchdowns', 0)
                receiving_tds = player.stats[week_number]['breakdown'].get('receivingTouchdowns', 0)
                passing_tds = player.stats[week_number]['breakdown'].get('passingTouchdowns', 0)

                total_tds_home += rush_tds + receiving_tds + passing_tds

        if box_score.home_team not in team_dict:
            team_dict[box_score.home_team] = 0
        team_dict[box_score.home_team] += total_tds_home

        for player in box_score.away_lineup:
            if player.slot_position != "D/ST" and player.slot_position != "BE":
                rush_tds = player.stats[week_number]['breakdown'].get('rushingTouchdowns', 0)
                receiving_tds = player.stats[week_number]['breakdown'].get('receivingTouchdowns', 0)
                passing_tds = player.stats[week_number]['breakdown'].get('passingTouchdowns', 0)

                total_tds_away += rush_tds + receiving_tds + passing_tds

        if box_score.away_team not in team_dict:
            team_dict[box_score.away_team] = 0
        team_dict[box_score.away_team] += total_tds_away


    top_team = max(team_dict, key=team_dict.get)
    top_team_tds = team_dict[top_team]

    if team_dict:
        return {
            'team_name': top_team.team_name,
            'top_team_tds': top_team_tds
        }
    else:
        return None


# Returns team with most points over their weekly projection with their starters for week 6
def week6_weekly(league):
    week_number = 6 #change this to 6
    top_team = None
    total_points_projected = 0
    total_points_actual = 0
    max_difference = -1

    box_scores = league.box_scores(week = week_number)
    for box_score in box_scores:
        home_team_actual_points = box_score.home_score
        home_team_projected_points = box_score.home_projected

        home_difference = home_team_actual_points - home_team_projected_points

        away_team_actual_points = box_score.away_score
        away_team_projected_points = box_score.away_projected

        away_difference = away_team_actual_points - away_team_projected_points

        if home_difference > max_difference:
            max_difference = home_difference
            top_team = box_score.home_team
            total_points_projected = box_score.home_projected
            total_points_actual = box_score.home_score
        if away_difference > max_difference:
            max_difference = away_difference
            top_team = box_score.away_team
            total_points_projected = box_score.away_projected
            total_points_actual = box_score.away_score

    if top_team:
        return {
            'team_name': top_team,
            'team_points_projected': total_points_projected,
            'team_points_actual': total_points_actual
        }
    else:
        return None

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
                        rushing_yards = player.stats[4]['breakdown'].get('rushingYards', 0)
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

                player_info = {
                    'player_name': player.name,
                    'data':player.stats
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

    if '!hello' == message:
        response_message = "Hi there! How can I assist you today?"
    elif '!fantasy' == message:
        fantasy_data = fetch_fantasy_data()
        if fantasy_data:
            response_message = f"Fantasy league data: {fantasy_data}"
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly1' == message:
        fantasy_data = week1_weekly(league)
        
        if fantasy_data:
            player_name = fantasy_data.get('player_name')
            player_points = fantasy_data.get('player_points')
            player_team = fantasy_data.get('player_team')
            response_message = f"Winner of Weekly 1: Get Schwifty - Team with the single highest scoring starter: \n\n{player_team} ({player_name} {player_points})" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    # weekly2 does not work
    elif '!weekly2' == message:
        fantasy_data = week2_weekly(league)
        # player_name = fantasy_data.get('qb_name')
        if fantasy_data:
            response_message = f"{fantasy_data}." 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly3' == message:
        fantasy_data = week3_weekly(league)
        
        if fantasy_data:
            team_name = fantasy_data.get('team_name')
            total_points = fantasy_data.get('bench_points')
            response_message = f"Winner of Weekly 3: Bench Warmer - Team with the most total points from their bench: \n\n{team_name} ({total_points} bench points)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly4' == message:
        fantasy_data = week4_weekly(league)
        
        if fantasy_data:
            team_name = fantasy_data.get('team_name')
            player_name = fantasy_data.get('player_name')
            player_rushing_yards = fantasy_data.get('player_rushing_yards')
            response_message = f"Winner of Weekly 4: Run Forrest Run! - Team with the starting RB with the most rushing yards: \n\n{team_name} ({player_name} {player_rushing_yards} rush yards)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly5' == message:
        fantasy_data = week5_weekly(league)
        
        if fantasy_data:
            team_name = fantasy_data.get('team_name')
            player_name = fantasy_data.get('player_name')
            player_points = fantasy_data.get('player_points')
            difference = fantasy_data.get('difference')
            response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly6' == message:
        fantasy_data = week6_weekly(league)
        
        if fantasy_data:
            team_name = fantasy_data.get('team_name')
            team__points_projected = fantasy_data.get('team_points_projected')
            team_points_actual = fantasy_data.get('team_points_actual')
            difference = team_points_actual - team__points_projected

            clean_team_name = team_name.team_name
            team__points_projected_formatted = f"{team__points_projected:.2f}"
            team_points_actual_formatted = f"{team_points_actual:.2f}"
            difference_formatted = f"{difference:.2f}"
            response_message = f"Winner of Weekly 6: Over Achiever - Team with most points over their weekly projections with their starters: \n\n{clean_team_name} (points projected: {team__points_projected_formatted} points, points actual: {team_points_actual_formatted} points, {difference_formatted} difference)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly7' == message:
        fantasy_data = week7_weekly(league)
        
        if fantasy_data:
            team_name = fantasy_data.get('team_name')
            team_total_tds = fantasy_data.get('top_team_tds')
            response_message = f"Winner of Weekly 7: Touchdown Thurman Thomas - Team with the most offensive touchdowns scored with their starters: \n\n{team_name} ({team_total_tds} tds)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly8' == message:
        fantasy_data = week8_weekly(league)

        if fantasy_data:
            team_name = fantasy_data.get("top_team")
            player_name = fantasy_data.get("top_player")
            player_points = fantasy_data.get("top_player_points")
            response_message = f"Winner of Weekly 8: Should have Swiped Right - Team with the highest scorer on the bench: \n\n{team_name} ({player_name} {player_points} points)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly9' == message:
        fantasy_data = week9_weekly(league)

        if fantasy_data:
            team_name = fantasy_data.get("top_team")
            difference = fantasy_data.get("difference")
            actual_score = fantasy_data.get("actual_score")
            projected_score = fantasy_data.get("projected_score")
            response_message = f"Winner of Weekly 9: Bulls-eye - Team closest to their projcted point total (over OR under): \n\n{team_name} (Projected: {projected_score} points, Actual: {actual_score} points, difference of {difference:.2f} points)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly10' == message:
        fantasy_data = week10_weekly(league)

        if fantasy_data:
            winning_team = fantasy_data.get("winning_team")
            winning_team_score = fantasy_data.get("winning_team_score")
            difference = fantasy_data.get("difference")
            losing_team = fantasy_data.get("losing_team")
            losing_team_score = fantasy_data.get("losing_team_score")
            response_message = f"Winner of Weekly 10: Blownout.com/rekt - Team that wins with the biggest points margin of victory: \n\n{winning_team} ({winning_team_score} points, won by {difference:.2f} vs {losing_team}, {losing_team_score} )" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly11' == message:
        fantasy_data = week11_weekly(league)

        if fantasy_data:
            top_loser = fantasy_data.get("top_loser")
            top_loser_score = fantasy_data.get("top_loser_score")
            response_message = f"Winner of Weekly 11: Best Loser - Team that loses with the highest score: \n\n{top_loser} (Lost with {top_loser_score} points)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly12' == message:
        fantasy_data = week12_weekly(league)
        if fantasy_data:
            top_teams = fantasy_data.get("top_teams")
            max_receptions = fantasy_data.get("max_receptions")
            message = []
            for team, player in top_teams.items():
                team_name = team.team_name
                player_name = player.name
                message_temp = f"{team_name} ({player_name}, {max_receptions} receptions)"
                message.append(message_temp)
            
            response_message = f"Winner of Weekly 12: Gotta Catch Em All - Teams with the starting WRs with the most receptions: \n\n" + "\n".join(message)
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly13' == message:
        fantasy_data = week13_weekly(league)
        if fantasy_data:
            response_message = f"{fantasy_data}"
            # response_message = f"Winner of Weekly 13: Blackjack - Team with a starter closest to 21 points without going over: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly14' == message:
        fantasy_data = week14_weekly(league)
        if fantasy_data:
            response_message = f"{fantasy_data}"
            # response_message = f"Winner of Weekly 14: Photo Finish - Team that beats its opponent by the smallest margin of victory: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
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