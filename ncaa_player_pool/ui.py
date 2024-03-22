from typing import List
import hank_gathers as hank
from ipydatagrid import DataGrid
from player_stats import SquadRow
import pandas as pd
from tabulate import tabulate

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

    squads = hank.gather()
    col = ['player', 'team', 'rd1', 'rd2','rd3','rd4','rd5','rd6', 'total']

    html = """<html>
<style>
table, th, td {
  border: 1px solid;
}
</style>
</head>
<body>
"""
    for squad in squads:
        html += "<h2> Squad Leader: {0}</h2>".format(squad.coach)
        html += "<h3> total points: {0}</h3>".format(squad.totalPoints)
        table = "<table>\n<tbody>\n"
        table += "  <tr>\n"
        for header in col:
            table += "    <th>{0}</th>\n".format(header.strip())
        table += "  </tr>\n"
        for player in squad.players:
            table += "  <tr>\n"
            table += "    <td>{0}</td>\n".format(player.player.strip())
            table += "    <td>{0}</td>\n".format(player.team)
            for game in player.games:
                if game.round == 'First Round':
                    table += "    <td>{0}</td>\n".format(game.points)
                elif game.round == 'Second Round':
                    table += "    <td>{0}</td>\n".format(game.points)
                else: 
                    raise Exception('Unkown round {0}'.format(game.round))
            table += "  </tr>\n"
        table += "</tbody>\n</table>\n"
        html += "{0}\n".format(table)
    html += "</body>\n</html>"

    with open(outfile, 'w') as out:
        out.writelines(html)

def render_scores():
    data = get_scores()
    # df = pd.DataFrame(data)
    # print(tabulate(df, tablefmt='html'))
    output_html('./test/table.html')

if __name__ == "__main__":
    render_scores()