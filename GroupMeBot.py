from flask import Flask, request, jsonify
from espn_api.football import League
import requests
import config
import schedule
import random
import os
import time
import threading
import datetime

app = Flask(__name__)

# testing
def survival_bowl_scheduled():
  league = League(league_id=config.ESPN_LEAGUE_ID, year=config.ESPN_SEASON_YEAR)
  fantasy_data = survival_bowl(league)
  if fantasy_data:
      surviving_teams = fantasy_data.get("surviving_teams")
      dead_teams = fantasy_data.get("dead_teams")
      current_week = league.nfl_week - 1

      formatted_surviving_teams = "\n".join(f" - {team}" for team in surviving_teams)
      formatted_dead_teams = "\n".join(f" - {team}: ({score} points)" for team, score in dead_teams.items())
      formatted_response = (
          f"Survival Bowl\n"
          f"Lowest score each week is eliminated. Last team standing wins.\n\n"
          f"Week {current_week}\n"
          f"Surviving teams:\n{formatted_surviving_teams}\n\n"
          f"Eliminated teams:\n{formatted_dead_teams}"
      )

      response_message = formatted_response
      send_message(response_message) 
      return {"status": "OK", "response": response_message}
  else:
      response_message = "Sorry, I couldn't fetch the fantasy data."
      send_message(response_message) 
      return {"status": "OK", "response": response_message}

#testing
def schedule_survival_bowl():
    # Schedule the task (e.g., run every Monday at 10 AM)
    # Glitch uses UTC time zone not EST, so EST to UTC +4 hours 
    schedule.every().wednesday.at("12:16").do(survival_bowl_scheduled)
    # schedule.every(5).seconds.do(survival_bowl_scheduled)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every minute(60) if the job should run


def survival_bowl(league):
    current_week = league.nfl_week
    all_teams = league.teams
    surviving_teams = []
    dead_teams_dict = {}
    all_team_names_and_scores = {}
    for i in range(1, current_week):
        bottom_team = None
        all_team_names_and_scores.clear()
        box_scores = league.box_scores(week=i)
        for box_score in box_scores:
            home_team = box_score.home_team
            away_team = box_score.away_team
            all_team_names_and_scores[home_team] = box_score.home_score
            all_team_names_and_scores[away_team] = box_score.away_score
                
        # get rid of all teams where the key is an int (for some reason, teams eliminated they turn into ints, idk why)
        filtered_all_team_names_and_scores = {key: value for key, value in all_team_names_and_scores.items() if not isinstance(key, int)}
        bottom_team = min(filtered_all_team_names_and_scores, key=filtered_all_team_names_and_scores.get)
        dead_teams_dict
        dead_teams_score = filtered_all_team_names_and_scores[bottom_team]
        dead_teams_dict[bottom_team.team_name] = dead_teams_score
        all_teams.remove(bottom_team)

    for team in all_teams:
        surviving_teams.append(team.team_name)
    
    if all_teams:
        return {
            "surviving_teams": surviving_teams,
            "dead_teams": dead_teams_dict
        }
    else:
        return None

# Returns team that beats its opponent by the smallest margin of victory for week 14
def week14_weekly(league):
    week_number = 14
    winning_team = None
    winning_team_score = 0
    losing_team = None
    losing_team_score = 0
    min_difference = 500

    box_scores = league.box_scores(week=week_number)
    for box_score in box_scores:
        if box_score.home_score > box_score.away_score:
            difference_temp = abs(box_score.home_score - box_score.away_score)
            if difference_temp < min_difference:
                min_difference = difference_temp
                winning_team = box_score.home_team
                winning_team_score = box_score.home_score
                losing_team = box_score.away_team
                losing_team_score = box_score.away_score
        else:
            difference_temp = abs(box_score.home_score - box_score.away_score)
            if difference_temp < min_difference:
                min_difference = difference_temp
                winning_team = box_score.away_team
                winning_team_score = box_score.away_score
                losing_team = box_score.home_team
                losing_team_score = box_score.home_score
    
    return {
        "winning_team" : winning_team.team_name,
        "winning_team_score": winning_team_score,
        "losing_team" : losing_team.team_name,
        "losing_team_score": losing_team_score,
        "difference": min_difference
    }


# Returns team with a starter closest to 21 points without going over for week 13
# needs to be fixed in case of 2 players that are tied
def week13_weekly(league):
    week_number = 13
    top_player = None
    top_player_points = 0
    top_team = None
    blackjack = 21
    difference_target = 500

    box_scores = league.box_scores(week = week_number)

    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.slot_position != "BE" and player.slot_position != "IR":
                difference_temp = player.points - blackjack
                if difference_temp < difference_target and difference_temp >= 0:
                    difference_target = difference_temp
                    top_player = player
                    top_player_points = player.points
                    if top_player in box_score.home_lineup:
                        top_team = box_score.home_team.team_name
                    else:
                        top_team = box_score.away_team.team_name
    if top_player:
        return {
            "top_player": top_player.name,
            "top_player_points": top_player_points,
            "top_team": top_team
        }
    else:
        return None


# Returns team with the starting WR with the most receptions for week 12
def week12_weekly(league):
    week_number = 12
    top_teams = {}
    top_wrs = []
    all_wrs = {}
    max_receptions = 0

    box_scores = league.box_scores(week = week_number)

    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.slot_position == "WR" and player.slot_position != "BE" and player.slot_position != "IR":
                receptions = player.stats[week_number]['breakdown'].get('receivingReceptions', 0)
                all_wrs[player]  = receptions
    
    max_receptions = max(all_wrs.values())
    # max_receptions = 7
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
    week_number = 11
    top_loser = None
    top_loser_score = 0
    losing_teams = {}
    winning_team = None
    winning_team_score = 0

    box_scores = league.box_scores(week=week_number)
    
    for box_score in box_scores:
        if box_score.home_score < box_score.away_score:
            losing_teams[box_score.home_team] = box_score.home_score
        else:
            losing_teams[box_score.away_team] = box_score.away_score

    top_loser = max(losing_teams, key=losing_teams.get)
    top_loser_score = losing_teams[top_loser]

    for box_score in box_scores:
        if box_score.home_team == top_loser:
            winning_team = box_score.away_team
            winning_team_score = box_score.away_score
        elif box_score.away_team == top_loser:
            winning_team = box_score.home_team
            winning_team_score = box_score.home_score


    if top_loser:
        return {
            "top_loser" : top_loser.team_name,
            "top_loser_score" : top_loser_score,
            "winning_team": winning_team.team_name,
            "winning_team_score": winning_team_score
        }
    else:
        return None
    

# Returns team that wins with the bigest points of margin of victory for week 10
def week10_weekly(league):
    week_number = 10
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
    week_number = 9
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
    week_number = 8
    top_team = None
    top_player = None
    top_player_points = 0
    box_scores = league.box_scores(week = week_number)
    
    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.slot_position == "BE" and player.slot_position != "IR":
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
    week_number = 7
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
            if player.slot_position != "D/ST" and player.slot_position != "BE" and player.slot_position != "IR":
                rush_tds = player.stats[week_number]['breakdown'].get('rushingTouchdowns', 0)
                receiving_tds = player.stats[week_number]['breakdown'].get('receivingTouchdowns', 0)
                passing_tds = player.stats[week_number]['breakdown'].get('passingTouchdowns', 0)

                total_tds_home += rush_tds + receiving_tds + passing_tds

        if box_score.home_team not in team_dict:
            team_dict[box_score.home_team] = 0
        team_dict[box_score.home_team] += total_tds_home

        for player in box_score.away_lineup:
            if player.slot_position != "D/ST" and player.slot_position != "BE" and player.slot_position != "IR":
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
    week_number = 6 
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
            if player.position == "RB" and player.slot_position != "BE" and player.slot_position != "IR":
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

# Returns team with starter QB who threw the longest pass (touchdown or not) for week 2
def week2_weekly(league):
    week_number = 2 # change this to 2
    longest_pass = -1
    top_qb = None
    top_qb_team = None
    qb_and_longest_pass = {}

    # URL that gets the game logs of each player based on player_Id
    base_url = "https://site.web.api.espn.com/apis/common/v3/sports/football/nfl/athletes/{}/gamelog"

    box_scores = league.box_scores(week=week_number)
    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            # loop through all starting qbs id of each team
            if player.slot_position == "QB" and player.slot_position != "BE" and player.slot_position != "IR":
                qb_id = player.playerId
                url = base_url.format(qb_id)
                response = requests.get(url)
                if response.status_code == 200:
                    # Parse the JSON data
                    data = response.json()
                    # Access the second-to-last event, which means week 2 of regular season based on player_ID
                    week2_game = data["seasonTypes"][0]["categories"][0]["events"][-2]

                    # specific stat, which is longest pass based on player_ID
                    longest_pass_value = week2_game["stats"][7]

                    # add to dict qb player name and their longest pass
                    qb_and_longest_pass[player] = longest_pass_value

                    #go to the next team in loop

                else:
                    # Handle errors (e.g., if the athlete ID is not found or there's a server issue)
                    return f"Failed to retrieve data for athlete ID {qb_id}. Status code: {response.status_code}"

    # get top qb with the longest pass    
    top_qb = max(qb_and_longest_pass, key=qb_and_longest_pass.get)

    # get the value of the longest pass
    longest_pass = qb_and_longest_pass[top_qb]

    # get the team that has the qb with the longest pass
    for box_score in box_scores:
        for player in box_score.home_lineup + box_score.away_lineup:
            if player.slot_position == "QB" and player.slot_position != "BE" and player.slot_position != "IR":
                if top_qb in box_score.home_lineup:
                    top_qb_team = box_score.home_team.team_name
                else:
                    top_qb_team = box_score.away_team.team_name



    # Return the top QB information
    return {
        "top_qb": top_qb.name,
        "longest_pass": longest_pass,
        "team": top_qb_team
    }


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

# Returns one of the random responses from the list
def random_response():
    random_responses = [
        "bruhhhhhhhh idk what means",
        "Sheeeeeeeesh",
        "Skibidi toilet or something like that",
        "Ayoooooo",
        "That's wild",
        "NFL is rigged",
        "Pause",
        "I ain't readin all that",
        "No Fun League strikes again"
        ]
    return random.choice(random_responses)

# this method is for testing
def fetch_fantasy_data():
    try:
        # Initialize the league object
        league = League(league_id=config.ESPN_LEAGUE_ID, year=config.ESPN_SEASON_YEAR)
        team_data = []
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
    
    if 'bad bot' in message:
        response_message = "Bruh I’m just trying to help!"
        send_message(response_message) 
        return jsonify({"status": "OK", "response": response_message}), 200

    if 'good bot' in message:
        response_message = "Hell yea bruh!"
        send_message(response_message) 
        return jsonify({"status": "OK", "response": response_message}), 200


    if not message.startswith('!'):
            return "OK", 200

    if '!hello' == message:
        formatted_response = (
                f"Hi there! I'm Roger Goodell bot!\n\n"
                f"Use command, !commands to see what other commands I can do."
            )
        response_message = formatted_response
    elif '!commands' == message:
        formatted_response = (
                f"Here are the commands you can use\n\n"
                f" - !weekly# - where # is the week number. !weekly1 to find out who won the week 1 weekly, !weekly2 to find out who won the week 2 weekly and so on.\n\n"
                f" - !survival - to find out who is currently in the survival bowl.\n\n"
                f" - !hello - to say hi to the bot."
            )
        response_message = formatted_response
    elif '!fantasy' == message:
        fantasy_data = fetch_fantasy_data()
        if fantasy_data:
            response_message = f"Fantasy league data: {fantasy_data}"
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    elif '!weekly1' == message:
        weekly_week = 1
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week1_weekly(league)
            
            if fantasy_data:
                player_name = fantasy_data.get('player_name')
                player_points = fantasy_data.get('player_points')
                player_team = fantasy_data.get('player_team')
                response_message = f"Winner of Weekly 1: Get Schwifty - Team with the single highest scoring starter: \n\n{player_team} ({player_name} {player_points})" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 1 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly2' == message:
        weekly_week = 2
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week2_weekly(league)
            if fantasy_data:
                top_qb = fantasy_data.get("top_qb")
                longest_pass = fantasy_data.get("longest_pass")
                player_team = fantasy_data.get("team")

                response_message = f"Winner of Weekly 2: Chicks Dig The Long Ball - Team with the starting QB with the longest pass: \n\n{player_team} ({top_qb} {longest_pass} yard pass)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 2 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly3' == message:
        weekly_week = 3
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week3_weekly(league)
            
            if fantasy_data:
                team_name = fantasy_data.get('team_name')
                total_points = fantasy_data.get('bench_points')
                response_message = f"Winner of Weekly 3: Bench Warmer - Team with the most total points from their bench: \n\n{team_name} ({total_points} bench points)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 3 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly4' == message:
        weekly_week = 4
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week4_weekly(league)
            
            if fantasy_data:
                team_name = fantasy_data.get('team_name')
                player_name = fantasy_data.get('player_name')
                player_rushing_yards = fantasy_data.get('player_rushing_yards')
                response_message = f"Winner of Weekly 4: Run Forrest Run! - Team with the starting RB with the most rushing yards: \n\n{team_name} ({player_name} {player_rushing_yards} rush yards)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 4 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly5' == message:
        weekly_week = 5
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week5_weekly(league)
            
            if fantasy_data:
                team_name = fantasy_data.get('team_name')
                player_name = fantasy_data.get('player_name')
                player_points = fantasy_data.get('player_points')
                difference = fantasy_data.get('difference')
                response_message = f"Winner of Weekly 5: Dirty 30 - Team with any starter closest to 30 points: \n\n{team_name} ({player_name} {player_points} points, {difference} difference to 30)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 5 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly6' == message:
        weekly_week = 6
        current_week = league.current_week

        if weekly_week < current_week:
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
                response_message = f"Winner of Weekly 6: Over Achiever - Team with most points over their weekly projections with their starters: \n\n{clean_team_name} (points projected: {team__points_projected_formatted} points, points actual: {team_points_actual_formatted} points, difference: {difference_formatted} points)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 6 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly7' == message:
        weekly_week = 7
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week7_weekly(league)
            
            if fantasy_data:
                team_name = fantasy_data.get('team_name')
                team_total_tds = fantasy_data.get('top_team_tds')
                response_message = f"Winner of Weekly 7: Touchdown Thurman Thomas - Team with the most offensive touchdowns scored with their starters: \n\n{team_name} ({team_total_tds} tds)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 7 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly8' == message:
        weekly_week = 8
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week8_weekly(league)

            if fantasy_data:
                team_name = fantasy_data.get("top_team")
                player_name = fantasy_data.get("top_player")
                player_points = fantasy_data.get("top_player_points")
                response_message = f"Winner of Weekly 8: Should have Swiped Right - Team with the highest scorer on the bench: \n\n{team_name} ({player_name} {player_points} points)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 8 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly9' == message:
        weekly_week = 9
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week9_weekly(league)

            if fantasy_data:
                team_name = fantasy_data.get("top_team")
                difference = fantasy_data.get("difference")
                actual_score = fantasy_data.get("actual_score")
                projected_score = fantasy_data.get("projected_score")
                response_message = f"Winner of Weekly 9: Bulls-eye - Team closest to their projcted point total (over OR under): \n\n{team_name} (Projected: {projected_score} points, Actual: {actual_score} points, difference of {difference:.2f} points)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 9 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."
        
    elif '!weekly10' == message:
        weekly_week = 10
        current_week = league.current_week

        if weekly_week < current_week:
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
        else:
            response_message = "Week 10 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly11' == message:
        weekly_week = 11
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week11_weekly(league)

            if fantasy_data:
                top_loser = fantasy_data.get("top_loser")
                top_loser_score = fantasy_data.get("top_loser_score")
                winning_team = fantasy_data.get("winning_team")
                winning_team_score = fantasy_data.get("winning_team_score")
                response_message = f"Winner of Weekly 11: Best Loser - Team that loses with the highest score: \n\n{top_loser} (Lost with {top_loser_score} points vs {winning_team} {winning_team_score} points)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 11 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly12' == message:
        weekly_week = 12
        current_week = league.current_week

        if weekly_week < current_week:
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
        else:
            response_message = "Week 12 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly13' == message:
        weekly_week = 13
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week13_weekly(league)
            if fantasy_data:
                top_player = fantasy_data.get("top_player")
                top_player_points = fantasy_data.get("top_player_points")
                top_team = fantasy_data.get("top_team")

                response_message = f"Winner of Weekly 13: Blackjack - Team with a starter closest to 21 points without going over: \n\n{top_team} ({top_player} {top_player_points} points)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 13 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!weekly14' == message:
        weekly_week = 14
        current_week = league.current_week

        if weekly_week < current_week:
            fantasy_data = week14_weekly(league)
            if fantasy_data:
                winning_team = fantasy_data.get("winning_team")
                winning_team_score = fantasy_data.get("winning_team_score")
                losing_team = fantasy_data.get("losing_team")
                losing_team_score = fantasy_data.get("losing_team_score")
                difference = fantasy_data.get("difference")

                response_message = f"Winner of Weekly 14: Photo Finish - Team that beats its opponent by the smallest margin of victory: \n\n{winning_team} ({winning_team} {winning_team_score} points vs {losing_team} {losing_team_score} points, {difference:.2f} difference)" 
            else:
                response_message = "Sorry, I couldn't fetch the fantasy data."
        else:
            response_message = "Week 14 is not over yet.\n\nUse command:\n!commmands to see what other commands you can use."

    elif '!survival' == message:
        fantasy_data = survival_bowl(league)
        if fantasy_data:
            surviving_teams = fantasy_data.get("surviving_teams")
            dead_teams = fantasy_data.get("dead_teams")
            current_week = league.nfl_week - 1

            formatted_surviving_teams = "\n".join(f" - {team}" for team in surviving_teams)
            formatted_dead_teams = "\n".join(f" - {team}: ({score} points)" for team, score in dead_teams.items())
            formatted_response = (
                f"Survival Bowl\n"
                f"Lowest score each week is eliminated. Last team standing wins.\n\n"
                f"Week {current_week}\n"
                f"Surviving teams:\n{formatted_surviving_teams}\n\n"
                f"Eliminated teams:\n{formatted_dead_teams}"
            )

            response_message = formatted_response
        else:
            response_message = "Sorry, I couldn't fetch the fantasy data."
    else:
        response_message = random_response()
    

    send_message(response_message)
    return jsonify({"status": "OK", "response": response_message}), 200


def send_message(msg):
    base_url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id': config.BOT_ID,
        'text': msg
    }
    requests.post(base_url, json=data)


if __name__ == '__main__':
    print(datetime.datetime.now())
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_survival_bowl)
    scheduler_thread.daemon = True  # Daemon thread will exit when the main program exits
    scheduler_thread.start()
    # uncomment below to run in dev server
    app.run(debug=True)