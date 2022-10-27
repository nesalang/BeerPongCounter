import sys
from guizero import App, Text
class ClockLabel:
    def __init__(self, app, timeString, clockEventHandler, x, y):
        self.clockTickCounter = ClockTicksCounter(timeString)
        self.clock = Text(app, text = self.clockTickCounter.GetFormatedTime(), size=150, font = 'Times New Roman', bg='white', width = 8, height = 3, grid=[x, y + 1, 1, 2])
        self.clock.repeat(1000, self.UpdateClockDisplay)
        self.clockEventHandler = clockEventHandler

    def UpdateClockDisplay(self):
        self.clockEventHandler();
    
    def UpdateClock(self, value):
        self.clock.value = value 

    def ResetClock(self):
        self.clockTickCounter.ResetTicksCounter()

    def DisableClock(self):
        self.clock.disable()

class ScoreLabels:
    def __init__(self, app, color, alignment, scoreEventHandler, x, y):
        self.score = Text(app, text=1, size=150, font ="Times New Roman", color= color, grid=[x, y], width = 4)
        self.scoreEventHandler = scoreEventHandler
        self.RegisterCallBack()

    def ResetScore(self):
        self.score.value = 0

    def UpdateScore(self, score):
        self.score.value = score

    def RegisterCallBack(self):
        self.score.repeat(1000, self.scoreEventHandler)

    def DisableDisplay(self):
        self.score.cancel(self.scoreEventHandler)
        self.score.disable()
         
class ScoreLabelsLeft(ScoreLabels):
    def __init__(self, app, eventHandler, x, y):
        super().__init__(app, 'blue', 'left', eventHandler, x, y + 1)


class ScoreLabelsRight(ScoreLabels):
    def __init__(self, app, eventHandler, x, y):
        self.indicator = Text(app, text='.', size=150, font ="Times New Roman", color= 'black', grid=[x, y], width = 4)
        super().__init__(app, 'red', 'right', eventHandler, x, y + 1)

class ClockTicksCounter:
    def __init__(self, time):
        self.time = time
        self.ResetTicksCounter()

    def ResetTicksCounter(self):
        self.seconds = self.time * 60

    def UpdateTime(self):
        if self.seconds > 0:
            self.seconds -= 1

    def HasTimeExpired(self):
        return self.seconds <= 0
            
    def GetFormatedTime(self):
        mininutes = self.seconds // 60
        seconds = self.seconds % 60
        secondsInString = str(seconds) if seconds >= 10 else '0' + str(seconds)
        minutesString = '0' + str(mininutes) if mininutes < 10 else str(mininutes)
        timeString = minutesString + ' : ' + secondsInString 
        return timeString

    #def GetUpdatedTime(self):
    #    self.UpdateTime()
    #    return self.GetFormatedTime()

class ScoreSource:
    def __init__(self):
        self.count = 0

    def GetScore(self):
        self.count += 1
        return self.count

class Team:
    def __init__(self, teamName):
        self.name = teamName
        self.scoreSource = ScoreSource()

    def GetScore(self):
        return self.scoreSource.GetScore()

    def GetTeamName(self):
        return self.name

class Round:
    def __init__(self, team0, team1, gameClock): 
        self.gameClock = gameClock
        self.teams = {team0.GetTeamName() : team0, team1.GetTeamName() : team1 }
        self.teamsList = [team0, team1]

    def __iter__(self):
        self.teamIndex = 0
        return self

    def __next__(self):
        if self.teamIndex < len(self.teams):
            team = self.teamsList[self.teamIndex]
            self.teamIndex += 1
            return  team
        else:
            raise StopIteration

    def GetWinner(self):
        maxScore = 0
        winners = []
        for team in self.teams.values():
            if team.GetScore() > maxScore:
                winners = [team]
            elif team.GetScore() == maxScore:
                winners.append(team)
                
        return winners

    def GetScore(self, team):
        if team.GetTeamName() in self.teams:
            return self.teams[team.GetTeamName()].GetScore()
        else: 
            return 0

    def UpdateGameTime(self):
        if not self.gameClock.HasTimeExpired():
            self.gameClock.UpdateTime()
    
    def GetCurrentFormattedGameTime(self):
        return self.gameClock.GetFormatedTime()

    def IsGameOver(self):
        return self.gameClock.HasTimeExpired()

class Game:
    def __init__(self, time, rounds):
        self.time = time
        self.numberOfRounds = rounds
        self.currentRoundIndex = 0
        self.rounds = [Round(Team("Red"), Team("Blue"), ClockTicksCounter(time)) for _ in range(rounds)]
        self.hasNewRoundStarted = False
        self.app = App(title="Welcome To Pong Game!!!", layout='grid', width = 2200, height = 800)
        self.redTeamScore = ScoreLabelsRight(self.app, self.UpdateScoreBoard, 0, 0)
        self.blueTeamScore = ScoreLabelsLeft(self.app, self.UpdateScoreBoard, 0, 1)
        self.redTeamScore1 = ScoreLabelsRight(self.app, self.UpdateScoreBoard, 1, 0)
        self.blueTeamScore1 = ScoreLabelsLeft(self.app, self.UpdateScoreBoard, 1, 1)
        self.redTeamScore2 = ScoreLabelsRight(self.app, self.UpdateScoreBoard, 2, 0)
        self.blueTeamScore2 = ScoreLabelsLeft(self.app, self.UpdateScoreBoard, 2, 1)
        self.gameClockDisplay = ClockLabel(self.app, time, self.ManageGameTime, 3, 0)
        self.ScoreDisplays= { "Red" : self.redTeamScore, "Blue" : self.blueTeamScore };

    def ResetUI(self):
        self.redTeamScore.ResetScore()
        self.blueTeamScore.ResetScore()
        self.gameClockDisplay.ResetClock()

    def StartNewRound(self):
        print('a')
        if self.currentRoundIndex < len(self.rounds) - 1:
            print('b')
            self.currentRoundIndex += 1
            self.ResetUI()
            self.hasNewRoundStarted = True
        self.app.display()

    def ManageGameTime(self):
        if self.hasNewRoundStarted == False:
            return
        currentRound = self.rounds[self.currentRoundIndex]
        currentRound.UpdateGameTime()
        self.gameClockDisplay.UpdateClock(currentRound.GetCurrentFormattedGameTime())
        if currentRound.IsGameOver():
            winningTeam = currentRound.GetWinner()
            self.hasNewRoundStarted = False
            self.gameClockDisplay.DisableClock()
            self.redTeamScore.DisableDisplay()
            self.blueTeamScore.DisableDisplay()
            # Update UI to notify Winner

    def UpdateScoreBoard(self):
        currentRound = self.rounds[self.currentRoundIndex]
        if self.hasNewRoundStarted and not currentRound.IsGameOver():
            for eachTeam in currentRound:
                # get score label and update the score
                self.ScoreDisplays[eachTeam.GetTeamName()].UpdateScore(eachTeam.GetScore())

    def ComputeGameScoresForTeams(self):
        scores = {}
        for eachRound in self.rounds:
            for eachTeam in eachRound:
                if not eachTeam.GetTeamName() in scores:
                    scores[eachTeam.GetTeamName()] = 0
                scores[eachTeam.GetTeamName()] += eachTeam.GetScore()
        return scores

    def WhoHasWonTheGame(self, scores):
        winners = sorted(scores.items(), lambda x : x[1], reverse = True)
        if len(winners) > 0:
            if len(winners) == 1: 
                return [winners[0][0]]
            else:
                i = 0
                computedWinners = [winners[0][0]]
                while i + 1 < len(winners) and winners[i] == winners[i+1]:
                    computedWinners.append(winners[i+1][0])

                return computedWinners
        else:
            return []
        
def main():
    game = Game(1, 3)
    game.StartNewRound()
    return 0

if __name__ == '__main__':
    sys.exit(main())