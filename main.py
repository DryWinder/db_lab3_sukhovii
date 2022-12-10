import psycopg2
import matplotlib.pyplot as plt

username = 'postgres'
password = 'root1'
database = 'student01_DB'
host = 'localhost'
port = '5432'

query_1 = '''
CREATE VIEW query1 AS (SELECT player_name, (goals + assists) AS goals_and_assists FROM stats
JOIN players ON stats.player_id = players.player_id
ORDER BY goals_and_assists DESC);

'''

query_2 = '''
CREATE VIEW query2 AS (SELECT player_position, COUNT(player_position) AS num_positions FROM players
GROUP BY player_position
ORDER BY num_positions DESC);

'''

query_3 = '''
CREATE VIEW query3 AS (SELECT t1.team_name, SUM(t1.goals_and_assists) FROM (
SELECT teams.team_id, team_name, (goals + assists) AS goals_and_assists FROM teams
JOIN players ON teams.team_id = players.team_id
JOIN stats ON players.player_id = stats.player_id) AS t1
GROUP BY t1.team_name
ORDER BY SUM(goals_and_assists) DESC);

'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:

    cur1 = conn.cursor()
    cur1.execute('DROP VIEW IF EXISTS query1')
    cur1.execute(query_1)
    cur1.execute('SELECT * FROM query1')
    player_names = []
    goals_and_assists = []

    for row in cur1:
        player_names.append(row[0])
        goals_and_assists.append(row[1])

    cur2 = conn.cursor()
    cur2.execute('DROP VIEW IF EXISTS query2')
    cur2.execute(query_2)
    cur2.execute('SELECT * FROM query2')
    player_positions = []
    player_positions_amount = []

    for row in cur2:
        player_positions.append(row[0])
        player_positions_amount.append(row[1])

    cur3 = conn.cursor()
    cur3.execute('DROP VIEW IF EXISTS query3')
    cur3.execute(query_3)
    cur3.execute('SELECT * FROM query3')
    team_names = []
    goals_and_assists_amount = []

    for row in cur3:
        team_names.append(row[0])
        goals_and_assists_amount.append(row[1])


x_range = range(len(player_names))

bar = plt.bar(x_range, goals_and_assists, width=0.5)
plt.title('Кількість зроблених гольових дій(голів + асистів) грацями')
plt.xlabel('Гравці')
#plt.xticks(x_range, rotation=90, size=2)
plt.ylabel('Голи та асисти')

plt.tight_layout()
plt.show()


plt.pie(player_positions_amount, labels=player_positions, autopct='%1.1f%%')
plt.title('Частка кількості позицій гравців на футбольному полі в даній БД')
plt.show()


x_range = range(len(team_names))
plt.plot(x_range, goals_and_assists_amount, marker='o')
plt.xticks(x_range, team_names, size=10, rotation=90)
plt.title('Загальний обсяг гольових дій гравців кожної команди з даної БД')
plt.ylabel('Голи та асисти')
plt.xlabel('Назва команди')



plt.tight_layout()
plt.show()
