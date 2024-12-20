# GroupMe Fantasy Football bot
This is a GroupMe bot built with Python and Flask, utilizing [cwebdt94's Python ESPN API](https://github.com/cwendt94/espn-api) and the ESPN "Gamelog" API endpoint listed in [nntrn's espn-wiki repo](https://github.com/nntrn/espn-wiki), to send messages to a group chat in Groupme about Fantasy Football related data, deployed on [Glitch](https://glitch.com/~groupme-fantasy-football-bot-prod)

The bot's purpose is to respond with the winning team based on the "weekly" if you message the GroupMe chat where the bots lives with the command "!weekly#, where # is the week number.  
  
A "weekly" is an achievement for a team that meets a certain condition. If they meet it, they win that week's weekly.  
  
To get a response from the bot, you would type for example, "!weekly1" to find out the winner for the week 1 weekly.  
An example response would be "Winner of Weekly 1: Team Red - Team with the single highest scoring starter: Team Red (Patrick Mahomes 35 points)  
So the team that won the week 1 weekly is Team Red, because Patrick Mahomes scored 35 fantasy points.

### List of bot Commands
- !weekly<week number\> where <week number\> is the week number
    - Bot responds with the weekly of that week.
        - Example: !weekly1
- !survival
    - Bot responds with the list of surviving and eliminated teams for the surival bowl
- !week
    - Bot responds with current NFL week
- !commands
    - Bot responds with commands users can use
- !hello
    - Bot responds by introducing itself
- !<anything else\>
    - Bot responds with a random response
- "bad bot"
    - Bot responds negatively
- "good bot"
    - Bot responds positively

### The Weeklys are:  
- ✅ WEEK 1: Get Schwifty - Team with the single highest scoring starter   
- ✅ WEEK 2: Chicks Dig The Long Ball - Team with the starting QB with the longest pass   
- ✅ WEEK 3: Bench Warmer - Team with the most total points from their bench   
- ✅ WEEK 4: Run Forrest Run! - Team with the starting RB with the most rushing yards  
- ✅ WEEK 5: Dirty 30 - Team with any starter closest to 30 points (over OR under)  
- ✅ WEEK 6: Over Achiever: Team with most points over their weekly projection with their starters  
- ✅ WEEK 7: Touchdown Thurman Thomas - Team with the most offensive touchdowns scored with their starters  
- ✅ WEEK 8: Should Have Swiped Right - Team with the highest scorer on the bench  
- ✅ WEEK 9: Bulls-eye - Team closest to their projected point total (over OR under)  
- ✅ WEEK 10: Blownout.com/rekt - Team that wins with the biggest points margin of victory  
- ✅ WEEK 11: Best Loser - Team that loses with the highest score  
- ✅ WEEK 12: Gotta Catch Em All - Team with the starting WR with the most receptions    
- ✅ WEEK 13: Blackjack - Team with a starter closest to 21 points without going over  
- ✅ WEEK 14: Photo Finish – Team that beats its opponent by the smallest margin of victory  

### Other things to implement
- ✅ Survival Bowl
    - ✅ Every week, team with lowest score is eliminated from list of all teams. Last team standing wins.
- Playoff winners command
    - 3 division winners at end of season (top teams of each division)  
    - 3 wildcard winners at end of season  
- 1st, 2nd, 3rd, place command  
- Consolation prize command
    - Winner of consolation ladder
- ✅ Check if trying to get info on future weekly and to not give info yet if that week is not over.
- Schedule the weekly to trigger every Wednesday for current week and the survival bowl automatically
- ✅ Detects if somneone says "good bot" or "bad bot" and responds accordingly
- ✅ Added a random response to the else statement
- ✅ ~~Added ability to run bot a production server gunicorn when running on Glitch~~
    - got rid of this because of errors on Glitch
- Command to show list of weeklies

# What to do when new season starts
- Will add this in future but most likely have to edit config file. create a new bot, get new bot id, enter new league id, and enter new year

# How to test locally
1. Git clone into your machine  
2. Create a config.py in the same location as testGroupmeBot.py, and add your bot id, espn league id, and espn season year  
    - To get your bot id, login to the [GroupMe Developers site](https://dev.groupme.com/), log in or make an account, click on Bots, and you should find your Bot Id.
    - To get your espn league id, go to your espn fantasy page, and you should find it in the URL in this form:
        - https://fantasy.espn.com/football/team?leagueId=12345678&teamId=1
    - Format it in the config.py file in the form:
        - BOT_ID = 'asfd987sfda978'
        - ESPN_LEAGUE_ID = '12345678'
        - ESPN_SEASON_YEAR = 2024
3. Run the program with VSCode, making sure to have Flask, and espn_api installed on your machine
    - If theyre not installed on your machine use the commands:
        - pip install flask
        - pip install espn_api
4. To make requests to the bot locally, run Postman
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

# How to Deploy on Glitch
- Fork this repo
- Go to [Glitch](https://glitch.com/)
- Log in or make an account for Glitch
- Copy the HTTPS Clone link of the Forked repo. 
    - Example: https://github.com/John-Doe/GroupmeFantasyFootballBot.git
- Click New Project -> import from Github, paste the link in the popup
- Make the config.py file with the information:
    - BOT_ID = 'Your bot ID'
        - Go to [GroupMe Developers](https://dev.groupme.com/bots)
        - Log in or make an account
        - Click "Bots" at the top
        - Click "Create Bot"
        - Choose group chat your bot will live in
        - Name the bot
        - Enter CallBack URL
            - Example: https://your-project-name.glitch.me/
        - Click Submit
        - Click on bot you just made
        - Copy Bot ID
            - Example: 441076d3e670b76b9f03447eat
    - ESPN_LEAGUE_ID = 'Your League ID'
        - Go to Your ESPN Fantasy League
        - Copy League ID in the URL
            - Example: 12345678
                - You can find it in the URL: https://fantasy.espn.com/football/league/scoreboard?leagueId=12345678&matchupPeriodId=7&mSPID=7
    - ESPN_SEASON_YEAR = 2024
- The bot should now be live in your group chat.

# What I learned
* Python: Syntax related to routing, requests, and config
* Flask: How to use a microframework to build a bot
* APIs: How to connect to an API and use it to fetch ESPN Fantasy Football data
* Glitch: How to deploy a bot have it working
* Postman: How to test the bot and it's responses using Postman

# What I can improve on
* Python: Cleaner code, exception handling, logging.
* Functionality:   
    - ✅ Add weekly announcements based on that week's weekly. Example: week 1, team with starter with most points, and announce that in groupchat when giving a command in the format of !weekly#, where # is the week number. Example: !weekly2.  
    - ✅ Add weekly annoucnement based on survival bowl. Example: every week, eliminate team from list of who has the least amount of points. End of season only 1 team remains.  
    - Put logic for ties (2 teams have same score and how to resolve those ties) for all weeks.  
    - Consistent error checking for all weeks.
    - Maybe Defenses are not considered players and should not be counted.