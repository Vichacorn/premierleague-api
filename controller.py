from config import OPENAPI_AUTOGEN_DIR
import sys
sys.path.append(OPENAPI_AUTOGEN_DIR)

import pymysql as mysql
from config import DB_HOST, DB_USER, DB_PASSWD, DB_NAME
from openapi_server import models

def db_cursor():
    return mysql.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASSWD,db=DB_NAME)

def get_team():
    with db_cursor() as cs:
        cs.execute("""
        SELECT * FROM team
        """)

        result = [models.Team(*row) for row in cs.fetchall()]
        return result

def get_team_by_id(teamId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT * FROM team WHERE teamId = %s
        """,[teamId])
        
        result = models.Team(*cs.fetchone())
        return result

def get_team_by_array_id(teamId):
    result = []
    with db_cursor() as cs:
        for id in teamId:
            cs.execute("""
            SELECT * FROM team WHERE teamId = %s
            """,[id])
            result.append(cs.fetchone())

        return [models.Team(*row) for row in result]
        
def get_team_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT 	ranking.order,team.teamId,team.teamName, team.teamLogo,ranking.win, ranking.lose, ranking.draw , ranking.goalsDiff, ranking.points
        FROM   team
        INNER JOIN ranking 
        ON team.teamId = ranking.teamId
        WHERE ranking.seasonId = %s
        """,[seasonId])

        result = [models.TeamBySeason(*row) for row in cs.fetchall()]   
        return result

def get_shot_on_goal_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT team.teamId,team.teamName,team.teamLogo,AVG(home.shotOnGoal) AS avgShotOnGoal
    FROM (SELECT ranking.order,competition.home ,(statistic.shotsOnGoal->"$.home") AS shotOnGoal
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.home = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT ranking.order,competition.away ,(statistic.shotsOnGoal->"$.away") AS shotOngoal
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.away = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
      ORDER BY ranking.order
     ) AS away ON home.home = away.away
     INNER JOIN team ON home.home = team.teamId
     
     GROUP BY home.home
         """,[seasonId,seasonId])

        result = [models.TeamShotOnGoalBySeason(*row) for row in cs.fetchall()]   
        return result

def get_fouls_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT team.teamId,team.teamName,team.teamLogo,AVG(home.fouls) AS avgfouls
    FROM (SELECT ranking.order,competition.home ,(statistic.fouls->"$.home") AS fouls
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.home = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT ranking.order,competition.away ,(statistic.fouls->"$.away") AS fouls
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.away = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
      ORDER BY ranking.order
     ) AS away ON home.home = away.away
     INNER JOIN team ON home.home = team.teamId
     GROUP BY home.home
        """,[seasonId,seasonId])

        result = [models.TeamFoulsBySeason(*row) for row in cs.fetchall()]   
        return result

def get_ball_possession_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT team.teamId,team.teamName,team.teamLogo,AVG(home.BallPossession) AS avgBallPoessession
    FROM (SELECT ranking.order,competition.home ,(statistic.ballPossession->"$.home") AS BallPossession
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.home = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT ranking.order,competition.away ,(statistic.ballPossession->"$.away") AS BallPossession
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.away = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
      ORDER BY ranking.order
     ) AS away ON home.home = away.away
     INNER JOIN team ON home.home = team.teamId
     GROUP BY home.home
        """,[seasonId,seasonId])
        result = [models.TeamBallPossessionBySeason(*row) for row in cs.fetchall()]   
        return result

def get_goal_keeper_saves_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT team.teamId,team.teamName,team.teamLogo,AVG(home.goalKeeperSaves) AS avgGoalKeeperSaves
    FROM (SELECT ranking.order,competition.home ,(statistic.goalkeeperSaves->"$.home") AS goalKeeperSaves
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.home = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT ranking.order,competition.away ,(statistic.goalkeeperSaves->"$.away") AS goalKeeperSaves
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.away = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
      ORDER BY ranking.order
     ) AS away ON home.home = away.away
     INNER JOIN team ON home.home = team.teamId
     GROUP BY home.home
        """,[seasonId,seasonId])

        result = [models.TeamGoalKeeperSavesBySeason(*row) for row in cs.fetchall()]   
        return result

def get_blocked_shots_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT team.teamId,team.teamName,team.teamLogo,AVG(home.blockedShots) AS avgBlockedShots
    FROM (SELECT ranking.order,competition.home ,(statistic.blockedShots->"$.home") AS blockedShots
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.home = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT ranking.order,competition.away ,(statistic.blockedShots->"$.away") AS blockedShots
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.away = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
      ORDER BY ranking.order
     ) AS away ON home.home = away.away
     INNER JOIN team ON home.home = team.teamId
     GROUP BY home.home
        """,[seasonId,seasonId])

        result = [models.TeamBlockedShotsBySeason(*row) for row in cs.fetchall()]   
        return result

def get_total_passes_and_pass_accurate_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT team.teamId,team.teamName,team.teamLogo,AVG(home.totalPasses) AS avgtotalPasses, AVG(home.passAccurate) AS avgPassAccurate
    FROM (SELECT ranking.order,competition.home ,(statistic.totalPasses->"$.home") AS totalPasses, (statistic.passAccurate->"$.home") AS passAccurate
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.home = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT ranking.order,competition.away ,(statistic.totalPasses->"$.away") AS totalPasses, (statistic.passAccurate->"$.away") AS passAccurate
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.away = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
      ORDER BY ranking.order
     ) AS away ON home.home = away.away
     INNER JOIN team ON home.home = team.teamId
     GROUP BY home.home
        """,[seasonId,seasonId])

        result = [models.TeamPassBallBySeason(*row) for row in cs.fetchall()]   
        return result

def get_statistic_all_season_by_teamId(teamId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT home.seasonId, season.year, AVG(home.shotOnGoal) AS avgShotOnGoal,AVG(home.blockedShots) AS avgBlockedShots, AVG(home.fouls) AS avgFouls, AVG(home.ballPossession) AS avgBallPossession, AVG(home.goalKeeperSaves) AS avgGoalKeeperSaves,AVG(home.totalPasses) AS avgTotalPasses, AVG(home.passAccurate) AS avgPassAccurate
    FROM (SELECT competition.seasonId ,(statistic.shotsOnGoal->"$.home") AS shotOnGoal, (statistic.blockedShots->"$.home") AS blockedShots, (statistic.fouls->"$.home") AS fouls, (statistic.ballPossession->"$.home") AS ballPossession, 			(statistic.goalkeeperSaves->"$.home") AS goalKeeperSaves, (statistic.totalPasses->"$.home") AS totalPasses, (statistic.passAccurate->"$.home") AS passAccurate
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.seasonId = ranking.seasonId
	WHERE competition.home = %s AND competition.home = ranking.teamId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT competition.seasonId ,(statistic.shotsOnGoal->"$.away") AS shotOnGoal, (statistic.blockedShots->"$.away") AS blockedShots, (statistic.fouls->"$.away") AS fouls, (statistic.ballPossession->"$.away") AS ballPossession, 			(statistic.goalkeeperSaves->"$.away") AS goalKeeperSaves, (statistic.totalPasses->"$.away") AS totalPasses, (statistic.passAccurate->"$.away") AS passAccurate
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.seasonId = ranking.seasonId
	WHERE competition.away = %s AND competition.away = ranking.teamId
      ORDER BY ranking.order
     ) AS away ON home.seasonId = away.seasonId
     INNER JOIN season ON home.seasonId = season.seasonId
     GROUP BY home.seasonId
        """,[teamId,teamId])

        result = [models.StatisticOfTeamByTeamId(*row) for row in cs.fetchall()]   
        return result

