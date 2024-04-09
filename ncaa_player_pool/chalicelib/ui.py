from typing import List
import chalicelib.hank_gathers as hank
from chalicelib.player_stats import SquadRow, Squads, PlayerStats
from datetime import datetime, timezone
import pytz
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
                else: 
                    raise Exception('Unkown round {0}'.format(game.round))
            
            squadRows.append(sr)

    return squadRows

def output_html(): 
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
    highscore: int = 0
    ss = sorted(squads, key=lambda x: x.totalPoints, reverse=True)
    players: List[PlayerStats] = []
    html += "<h1> Leaderboard</h1>"
    html += "<h4> updated at {0}</h4>".format(dt)
    for squad in ss:
        html += "<h2> Squad Leader: {0}</h2>".format(squad.coach)
        html += "<h3> Total points: {0}</h3>".format(squad.totalPoints)
        if rows == 0:
            highscore = squad.totalPoints
        else:
            pointsBack = highscore - squad.totalPoints
            html += "<h4> Trailing by: {0}</h4>".format(pointsBack)
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
                    player.stillPlaying = False
                else:
                    gc += "    <td>{0}</td>\n".format(game.points)                

                i+=1
            player.squadCoach = squad.coach
            players.append(player)

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
    
    html += "<h2> Top Scorers </h2>"

    avgTable: str = "<table>\n<tbody>\n"
    avgTable += "  <tr>\n"
    avgTable += "    <th>player</th>"
    avgTable += "    <th>team</th>"
    avgTable += "    <th>squad leader</th>"
    avgTable += "    <th>total</th>"
    avgTable += "    <th>games</th>"
    avgTable += "    <th>avg.</th>"
    avgTable += "  </tr>\n"

    for player in sorted(players, key=lambda player: player.totalPoints, reverse=True):
        boxClass = 'normal'

        if not player.stillPlaying:
            boxClass = 'red-box'

        avgTable += "  <tr>\n"
        avgTable += "    <td class='{0}'>{1}</td>".format(boxClass, player.player)
        avgTable += "    <td class='{0}'>{1}</td>".format(boxClass, player.team)
        avgTable += "    <td class='{0}'>{1}</td>".format(boxClass, player.squadCoach)
        avgTable += "    <td class='{0}'>{1}</td>".format(boxClass, player.totalPoints)
        avgTable += "    <td class='{0}'>{1}</td>".format(boxClass, len(player.games))
        avgTable += "    <td class='{0}'>{1:.1f}</td>".format(boxClass, player.averagePoints)
        avgTable += "  </tr>\n"
    avgTable += "</tbody>\n</table>\n"

    html += "{0}\n".format(avgTable)
    html += "</body>\n</html>"
    return html

def render_scores(output_file: str = './test/index.html') -> str:
    with open(output_file, 'w') as out:
        out.writelines(output_html())
    
    return output_file

if __name__ == "__main__":
    render_scores()