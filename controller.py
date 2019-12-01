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
        SELECT home.home,AVG(home.shotOnGoal) AS avgShotOnGoal
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
     GROUP BY home.home 
         """,[seasonId,seasonId])

        result = [models.TeamShotOnGoalBySeason(*row) for row in cs.fetchall()]   
        return result

def get_fouls_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT home.home,AVG(home.fouls) AS avgfouls
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
     GROUP BY home.home
        """,[seasonId,seasonId])

        result = [models.TeamFoulsBySeason(*row) for row in cs.fetchall()]   
        return result

def get_ball_possession_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT home.home,AVG(home.BallPossession) AS avgBallPoessession
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
     GROUP BY home.home
        """,[seasonId,seasonId])
        result = [models.TeamBallPossessionBySeason(*row) for row in cs.fetchall()]   
        return result

def get_passed_percentage_by_season(seasonId):
    with db_cursor() as cs:
        cs.execute("""
        SELECT home.home,AVG(home.passedPercentage) AS avgPassedPercentage
    FROM (SELECT ranking.order,competition.home ,(statistic.passedPercentage->"$.home") AS passedPercentage
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.home = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
          ORDER BY ranking.order
     ) AS home INNER JOIN
     (SELECT ranking.order,competition.away ,(statistic.passedPercentage->"$.away") AS passedPercentage
	FROM competition
	INNER JOIN statistic ON competition.compId = statistic.statisticId
    INNER JOIN ranking ON competition.away = ranking.teamId
	WHERE ranking.seasonId = %s AND ranking.seasonId = competition.seasonId
      ORDER BY ranking.order
     ) AS away ON home.home = away.away
     GROUP BY home.home
        """,[seasonId,seasonId])

        result = [models.TeamPassedPercentageBySeason(*row) for row in cs.fetchall()]   
        return result