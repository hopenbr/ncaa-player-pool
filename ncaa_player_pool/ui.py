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
                elif game.round.startswith('Sweet'):
                    sr.round3 = game.points
                elif game.round.startswith('Elite'):
                    sr.round4 = game.points
                elif game.round.startswith('FINAL'):
                    sr.round5 = game.points
                elif game.round.startswith('Championship'):
                    sr.round6 = game.points
                else: 
                    raise Exception('Unkown round {0}'.format(game.round))
            
            squadRows.append(sr)

    return squadRows

def output_html(outfile: str): 
    est = pytz.timezone('US/Eastern')
    squads: Squads = hank.gather()
    col = ['player', 'team', 'r64', 'r32','r16','rd8','rd4','Chp', 'total']
    dt = datetime.now(est).strftime('%c')

    html = """<html>
<style>
table, th, td {
  border: 1px solid;
}

.normal {  
    border: 1px solid;  
}

.strike {
    text-decoration: line-through;
}

.live {
    color: green;
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
            rowClass = 'normal'
            totalPointClass = 'normal'
            for game in player.games:
                if game.status == 'live':
                    rowClass = 'live'
                    gc += "     <td class='{0}'>{1}</td>\n".format(rowClass, game.points)
                elif not game.winner:
                    rowClass = "strike"
                    totalPointClass = "red-box"
                    gc += "    <td>{0}</td>\n".format(game.points)
                else:
                    gc += "    <td>{0}</td>\n".format(game.points)                

                i+=1
               
            
            for f in range(6-i):
                gc += "    <td></td>\n"
            
            table += "  <tr>\n"
                
            gc += "    <td class='{0}'>{1}</td>\n".format(totalPointClass, player.totalPoints)
            table += "    <td class='{0}'>{1}</td>\n".format(rowClass, player.player.strip())
            table += "    <td class='{0}'>{1}</td>\n".format(rowClass, player.team)
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