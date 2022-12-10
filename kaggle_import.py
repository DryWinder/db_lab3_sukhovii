import pandas as pd
import psycopg2

username = 'postgres'
password = 'root1'
database = 'student01_DB'
host = 'localhost'
port = '5432'



data = pd.read_csv(r'C:\Users\Windows\Desktop\Tree\КПІ\5 semestr\Бази Даних\Dataset\key_stats.csv')

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

df = pd.DataFrame(data, columns=['club'])

unique_clubs = []
for i, item in df.iteritems():
    unique_clubs = item.unique()



cur1 = conn.cursor()

for i in range(len(unique_clubs)):
    query1 = "INSERT INTO teams(team_name) VALUES ('%s')" % unique_clubs[i]
    cur1.execute(query1)



cur2 = conn.cursor()

df = pd.DataFrame(data, columns=['player_name', 'position', 'club'])
pl_name = df['player_name']
pl_position = df['position']
pl_club = df['club']

for i in range(len(pl_name)):
    query2 = """
    INSERT INTO players(player_name, player_position, team_id)
    VALUES
    (('%s'), ('%s'), (SELECT team_id FROM teams WHERE (team_name = ('%s'))));
    """ % (pl_name[i], pl_position[i], pl_club[i])
    cur2.execute(query2)

conn.commit()

cur3 = conn.cursor()
data1 = pd.read_csv(r'C:\Users\Windows\Desktop\Tree\КПІ\5 semestr\Бази Даних\Dataset\disciplinary.csv')
df = pd.DataFrame(data, columns=['goals', 'assists', 'player_name'])
df1 = pd.DataFrame(data1, columns=['match_played', 'red', 'yellow'])

pl_goals = df['goals']
pl_assists = df['assists']
pl_mp = df1['match_played']
pl_red = df1['red']
pl_yellow = df1['yellow']
pl_name = df['player_name']


for i in range(len(pl_mp)):
    query3 = """
    INSERT INTO stats(matches_played, goals, assists, yellow_cards, red_cards, player_id)
    VALUES
    (('%s'), ('%s'), ('%s'), ('%s'), ('%s'), (SELECT player_id FROM players WHERE player_name = ('%s')));
    """ % (pl_mp[i], pl_goals[i], pl_assists[i], pl_yellow[i], pl_red[i], pl_name[i])
    cur3.execute(query3)

conn.commit()

