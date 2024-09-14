# Replace with actual values
LEAGUE_ID = 12345
ESPN_S2 = 'YOUR_ESPN_S2'
SWID = 'YOUR_SWID'
BASE_URL = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{seasonId}/segments/0/leagues/{leagueId}'

def fetch_data(season_id, matchup_period_id, scoring_period_id):
    url = BASE_URL.format(seasonId=season_id, leagueId=LEAGUE_ID)
    headers = {
        'Cookie': f'ESPN_S2={ESPN_S2}; SWID={SWID}',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Request failed: {response.status_code}")