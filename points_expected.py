import glob
import sys

def add_points(team, points):
	global team_points
	try:
		updated = team_points[team][-1] + points
		team_points[team].append(updated)
	except:
		team_points[team] = [0] # with 0 gp, points is 0
		team_points[team].append(points)


games_played = []
for i in range(83):
	games_played.append({})

for season in glob.glob("*csv"):
	team_points = {}
	with open(season, 'r') as schedule:
		for line in schedule:
			if line[0:4] != "Date":
				game = line.split(",")
				away = game[1]
				away_goals = game[2]
				away_points = 0
				
				home = game[3]
				home_goals = game[4]
				home_points = 0
				
				OT = True
				if (game[5] == ""):
					OT = False
					
				if away_goals > home_goals:
					away_points = 2
					if OT:
						home_points = 1
				elif home_goals > away_goals:
					home_points = 2
					if OT:
						away_points = 1
				else: # before the lockout there were ties
					home_points = 1
					away_points = 1
				
				add_points(away, away_points)
				add_points(home, home_points)
					

	for team in team_points.keys():
		for i in range(83):
			try:
				games_played[i][team_points[team][i]].append(team_points[team][-1])
			except:
				games_played[i][team_points[team][i]] = []
				games_played[i][team_points[team][i]].append(team_points[team][-1])

with open("expected_points.json", 'w') as out:
	out.write("{\"data\": [\n")
	for i in range(83):
		num_points = len(games_played[i].keys())
		j = 1
		for points in games_played[i].keys():
			out.write("{\"Games_Played\": ")
			out.write(str(i) + ",\n")
			out.write("\"Points\": " + str(points) + "}")
			if j < num_points or i != 82:
				out.write(",\n")
			else:
				out.write("\n")
			j += 1
	out.write("]}")
























	