import os
import sys
import json
import logging
import argparse
import requests
from player_stats import PlayerStats, Game, Squad, Squads
from typing import List
import time


def cli(args=None):
    exit_code: int = 0
    boxScoreUrl = "https://data.ncaa.com/casablanca{0}/boxscore.json"
    squads: Squads = []
    playerStats: List[PlayerStats] = []
    currentSquad: Squad = None

    try:
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
        dayOneGamesUrl = 'https://data.ncaa.com/casablanca/scoreboard/basketball-men/d1/2024/03/21/scoreboard.json'

        dayOneGames = requests.get(dayOneGamesUrl).json()['games']
        
        for dog in dayOneGames:
            game = dog['game']
            bsUrl = boxScoreUrl.format(game['url'])
            boxScore: dict = requests.get(bsUrl).json()
            #time.sleep(1)
            #check games that have not started do not have boxscores
            if 'teams' in boxScore.keys():
                for team in boxScore['teams']:
                    tid: str = '{0}'.format(team['teamId']) #force to string vs int 
                    teamName = [t for t in boxScore['meta']['teams'] if t['id'] == tid][0]['shortName']

                    for player in team['playerStats']:
                        points = player['points']
                        g = Game(date=game['startDate'], game=game['title'], round=game['bracketRound'], points=points)

                        playerName = '{0} {1}'.format(player['firstName'], player['lastName'])
                        #ps: PlayerStats = next((p.player == playerName for p in playerStats), None)
                        foundPlayer: bool = False
                        for s in squads:
                            for p in s.players:
                                if p.player == playerName and teamName == p.team:
                                    p.games.append(g)
                                    foundPlayer = True
                                    break
                                if foundPlayer:
                                    break
            else:
                logging.warn("Boxscore has not teams")
        for s in squads:
            print(s.model_dump_json())
    except Exception as e:
        exit_code = 1
        logging.fatal(f"{e}", exc_info=True)

    ##sys.exit(exit_code)

if __name__ == "__main__":
    cli()
