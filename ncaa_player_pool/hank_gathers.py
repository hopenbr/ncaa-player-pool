import os
import sys
import json
import logging
import argparse
import requests
from player_stats import PlayerStats, Game, Squad, Squads
from typing import List
import time
from datetime import datetime


def bracketDates() -> List[str]:
    dates: List[str] = ['2024/03/21', '2024/03/22', '2024/03/23', '2024/03/24',
                        '2024/03/28', '2024/03/29', '2024/03/30', '2024/03/31',
                        '2024/04/04', '2024/04/05', '2024/04/06', '2024/04/07',
                        '2024/04/11', '2024/04/12', '2024/04/13', '2024/04/15']
    
    validDates: List[str] = []
    today = datetime.today().date()

    for d in dates:
        dt = datetime.strptime(d, '%Y/%m/%d').date()
        if dt <= today:
            validDates.append(d)

    return validDates

def gather(args=None):
    exit_code: int = 0
    boxScoreUrl = "https://data.ncaa.com/casablanca{0}/boxscore.json"
    squads: Squads = []
    playerStats: List[PlayerStats] = []
    currentSquad: Squad = None

    logging.info('populating squads')
    with open('ncaa_player_pool/squads.json', 'r') as info:
        squadData = json.load(info)

    for squad in squadData:
        p = PlayerStats(player=squad['Player'], team=squad['Team'], games=[])

        if currentSquad and currentSquad.coach == squad['coach']:
            currentSquad.players.append(p)
        else:
            currentSquad = Squad(coach=squad['coach'], players=[p])
            squads.append(currentSquad)
            

    logging.info('starting...')

    for gameDay in bracketDates(): 

        gameDayUrl = 'https://data.ncaa.com/casablanca/scoreboard/basketball-men/d1/{0}/scoreboard.json'.format(gameDay)

        currentGames = requests.get(gameDayUrl).json()['games']
        
        for cg in currentGames:
            game = cg['game']
            bsUrl = boxScoreUrl.format(game['url'])
            boxScore: dict = requests.get(bsUrl).json()
            #time.sleep(1)
            #check games that have not started do not have boxscores
            if 'teams' in boxScore.keys():
                for team in boxScore['teams']:
                    tid: str = '{0}'.format(team['teamId']) #force to string vs int 
                    teamName = [t for t in boxScore['meta']['teams'] if t['id'] == tid][0]['seoName']

                    for player in team['playerStats']:
                        points = player['points']
                        g = Game(date=game['startDate'], game=game['title'], round=game['bracketRound'], points=points)

                        playerName = '{0} {1}'.format(player['firstName'], player['lastName'])
                        #ps: PlayerStats = next((p.player == playerName for p in playerStats), None)
                        foundPlayer: bool = False
                        for s in squads:
                            for p in s.players:
                                if p.player.lower() == playerName.lower() and teamName == p.team.lower():
                                    p.games.append(g)
                                    foundPlayer = True
                                    break
                                if foundPlayer:
                                    break
            else:
                logging.warn("Boxscore has no teams, game most likely hasn't started yet")
    return squads

def hank(args=None):
    try:
        for s in gather():
            print(s.model_dump_json())
    except Exception as e:
        exit_code = 1
        logging.fatal(f"{e}", exc_info=True)
    ##sys.exit(exit_code)

if __name__ == "__main__":
    hank()
