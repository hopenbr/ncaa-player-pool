from typing import List
import hank_gathers as hank
from ipydatagrid import DataGrid
from player_stats import SquadRow, Squads
import pandas as pd
from datetime import datetime, timezone
import pytz
import time
from tzlocal import get_localzone

def get_scores(): 

    squads = hank.gather()
    squadRows: List[SquadRow] = []
    for squad in squads:
        for player in squad.players:
            sr: SquadRow = SquadRow(coach=squad.coach, player=player.player, team=player.team)

            for game in player.games:
                if game.round == 'First Round':
                    sr.round1 = game.points
                elif game.round == 'Second Round':
                    sr.round2 = game.points
                else: 
                    raise Exception('Unkown round {0}'.format(game.round))
            
            squadRows.append(sr)

    return squadRows

def output_html(outfile: str): 
    est = pytz.timezone('US/Eastern')
    squads: Squads = hank.gather()
    col = ['player', 'team', 'rd1', 'rd2','rd3','rd4','rd5','rd6', 'total']
    dt = datetime.now(est).strftime('%c')

    html = """<html>
<style>
table, th, td {
  border: 1px solid;
}

.strike {
    text-decoration: line-through;
    border: 1px solid;
}

.red-box {
    color: white;
    background-color: red;
    border: 1px solid;
  }

</style>
</head>
<body>
"""
    rows: int = 0
    ss = sorted(squads, key=lambda x: x.totalPoints, reverse=True)
    html += "<h1> Leaderboard</h1>"
    html += "<h4> updated at {0}</h4>".format(dt)
    for squad in ss:
        html += "<h2> Squad Leader: {0}</h2>".format(squad.coach)
        html += "<h3> total points: {0}</h3>".format(squad.totalPoints)
        table = "<table>\n<tbody>\n"
        table += "  <tr>\n"
        for header in col:
            table += "    <th>{0}</th>\n".format(header.strip())
        table += "  </tr>\n"
        for player in squad.players:
            lost: bool = False
            i: int = 0
            gc: str = ''
            for game in player.games:
                if game.round == 'First Round':
                    gc += "    <td>{0}</td>\n".format(game.points)
                elif game.round == 'Second Round':
                    gc += "    <td>{0}</td>\n".format(game.points)
                else: 
                    raise Exception('Unkown round {0}'.format(game.round))
                i+=1
                if not game.winner:
                    lost = True
            
            for f in range(6-i):
                gc += "    <td></td>\n"
            
            table += "  <tr>\n"

            if lost:
                gc += "    <td class='red-box'>{0}</td>\n".format(player.totalPoints)
                table += "    <td class='strike'>{0}</td>\n".format(player.player.strip())
                table += "    <td class='strike'>{0}</td>\n".format(player.team)
            else:
                gc += "    <td>{0}</td>\n".format(player.totalPoints)
                table += "    <td>{0}</td>\n".format(player.player.strip())
                table += "    <td>{0}</td>\n".format(player.team)

            table += gc
            table += "  </tr>\n"
            rows+=1
        table += "</tbody>\n</table>\n"
        html += "{0}\n".format(table)
    html += "</body>\n</html>"

    with open(outfile, 'w') as out:
        out.writelines(html)

def render_scores():
    data = get_scores()
    # df = pd.DataFrame(data)
    # print(tabulate(df, tablefmt='html'))
    output_html('./test/index.html')

if __name__ == "__main__":
    render_scores()