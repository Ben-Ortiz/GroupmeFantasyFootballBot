# GroupMe Fantasy Football bot
This is a bot built with python and flask, utilizing [cwebdt94's Python ESPN API](https://github.com/cwendt94/espn-api), to send messages to a group chat in Groupme about Fantasy Football related data, deployed on [Glitch](https://glitch.com)

The bot's purpose is to respond with the winning team based on the "weekly".  
A "weekly" is an achievement for a team that meets a certain condition. If they meet it, they win that week's weekly.  
  
To get a response from the bot, you would type for example, "!weekly1" to find out the winner for the week 1 weekly.  
An example response would be "Winner of Weekly 1: Team Red - Team with the single highest scoring starter: Team Red (Patrick Mahomes 35 points)  
So the team that won the week 1 weekly is Team Red, because Patrick Mahomes scored 35 fantasy points.

### The Weeklys are:  
* WEEK 1: Get Schwifty - Team with the single highest scoring starter   
* WEEK 2: Chicks Dig The Long Ball - Team with the starting QB with the longest pass   
* WEEK 3: Bench Warmer - Team with the most total points from their bench   
* WEEK 4: Run Forrest Run! - Team with the starting RB with the most rushing yards  
* WEEK 5: Dirty 30 - Team with any starter closest to 30 points (over OR under)  
* WEEK 6: Over Achiever: Team with most points over their weekly projection with their starters  
* WEEK 7: Touchdown Thurman Thomas - Team with the most offensive touchdowns scored with their starters  
* WEEK 8: Should Have Swiped Right - Team with the highest scorer on the bench  
* WEEK 9: Bulls-eye - Team closest to their projected point total (over OR under)  
* WEEK 10: Blownout.com/rekt - Team that wins with the biggest points margin of victory  
* WEEK 11: Best Loser - Team that loses with the highest score  
* WEEK 12: Gotta Catch Em All - Team with the WR with the most receptions (bench players don't count)  
* WEEK 13: Blackjack - Team with a starter closest to 21 points without going over  
* WEEK 14: Photo Finish – Team that beats its opponent by the smallest margin of victory  

# How to test
1. Git clone into your machine  
2. Create a config.py in the same location as testGroupmeBot.py, and add your bot id, espn league id, and espn season year  
    1. To get your bot id, login to the GroupMe Developers site, click on Bots, and you should find your Bot Id.
    2. To get your espn league id, go to your espn fantasy page, and you should find it in the URL in this form:
        - https://fantasy.espn.com/football/team?leagueId=12345678&teamId=1
    3. Format it in the config.py file in the form:
        - BOT_ID = 'asfd987sfda978'
        - ESPN_LEAGUE_ID = '12345678'
        - ESPN_SEASON_YEAR = 2024
    4. Run the program, making sure to have Flask, and espn_api installed on your machine
        - If theyre not installed on your machine use the commands:
            - pip install flask
            - pip install espn_api
    5. To make requests to the bot locally, run Postman
        - Run a POST request to http://127.0.0.1:5000
        - Go to Headers
            - Key: "Content-type"
            - Value: "application/json"
        - Go to Body
            - enter a JSON object with:
                - "sender_type": "user"
                - "text": "!weekly3"
        - Send Request
            - Example Response:
                - Winner of Weekly 3 Bench Warmer - Team with the most total points from their bench: \n\nTeam Red (88.10 bench points)

# What I learned
* Python: Syntax related to routing, requests, and config
* Flask: How to use a microframework to build a bot
* APIs: How to connect to an API and use it to fetch ESPN Fantasy Football data
* Glitch: How to deploy a bot have it working
* Postman: How to test the bot and it's responses using Postman

# What I can improve on
* Python: Cleaner code, exception handling, logging.
* Functionality:   
- [ ] Add weekly announcements based on that week's weekly. Example: week 1, team with starter with most points, and announce that in groupchat.  
- [ ] Add weekly annoucnement based on survival bowl. Example: every week, eliminate team from list of who has the least amount of points. End of season only 1 team remains.  