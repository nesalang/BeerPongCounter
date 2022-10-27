import sys
from guizero import App, Text, PushButton
class ClockLabel:
    def __init__(self, app, timeString, clockEventHandler, x, y):
        self.clock = Text(app, text = timeString, size=150, font = 'Times New Roman', bg='white', width = 8, height = 3, grid=[x, y + 1, 1, 2])
        self.clock.repeat(1000, self.UpdateClockDisplay)
        self.clockEventHandler = clockEventHandler

    def UpdateClockDisplay(self):
        self.clockEventHandler()
    
    def UpdateClock(self, value):
        self.clock.value = value 

    def DisableClock(self):
        self.clock.disable()
        self.clock.cancel(self.UpdateClockDisplay)

    def EnableClock(self):
        self.clock.enable()
        self.clock.repeat(1000, self.UpdateClockDisplay)

class ScoreLabels:
    def __init__(self, app, color, alignment, scoreEventHandler, x, y):
        self.score = Text(app, text=0, size=150, font ="Times New Roman", color= color, grid=[x, y], width = 4)
        self.scoreEventHandler = scoreEventHandler
        self.score.disable()

    def ResetScore(self):
        self.DisableDisplay()

    def UpdateScore(self, score):
        self.score.value = score

    def RegisterCallBack(self):
        self.score.repeat(1000, self.scoreEventHandler)

    def DisableDisplay(self):
        #self.score.cancel(self.scoreEventHandler)
        self.score.disable()

    def EnableDisplay(self):
        self.score.enable()
        #self.RegisterCallBack()
         
class ScoreLabelsLeft(ScoreLabels):
    def __init__(self, app, eventHandler, x, y):
        super().__init__(app, 'blue', 'left', eventHandler, x, y + 1)


class ScoreLabelsRight(ScoreLabels):
    def __init__(self, app, eventHandler, x, y):
        self.indicator = Text(app, text='', size=150, font ="Times New Roman", color= 'black', grid=[x, y], width = 4)
        super().__init__(app, 'red', 'right', eventHandler, x, y + 1)
    def DisableDisplay(self):
        super().DisableDisplay()
        self.indicator.value = ''

    def EnableDisplay(self):
        super().EnableDisplay()
        self.indicator.value = '.'

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
        self.time = ClockTicksCounter(time)
        self.numberOfRounds = rounds
        self.currentRoundIndex = -1 
        self.RedTeam = Team("Red")
        self.BlueTeam = Team("Blue")
        self.hasNewRoundStarted = False
        self.app = App(title="Welcome To Pong Game!!!", layout='grid', width = 2200, height = 800)
        self.RedTeamScoreBoards = [ScoreLabelsRight(self.app, self.UpdateScoreBoard, i, 0) for i in range(3)]
        self.BlueTeamScoreBoards = [ScoreLabelsLeft(self.app, self.UpdateScoreBoard, i, 1) for i in range(3)]
        self.gameClockDisplay = ClockLabel(self.app, self.time.GetFormatedTime(), self.ManageGameTime, 3, 0)
        self.gameClockDisplay.DisableClock()
        self.StartStopButton = PushButton(self.app, text = 'Start Next Round', command= self.StartNewRound, grid = [0, 3])
        self.BeginNewGame = PushButton(self.app, text = 'Start New Game', grid = [1, 3])
        self.app.display()

    def UpdatePreviousRound(self) :
        if self.currentRoundIndex > 0:
            self.RedTeamScoreBoards[self.currentRoundIndex - 1].DisableDisplay()
            self.BlueTeamScoreBoards[self.currentRoundIndex - 1].DisableDisplay()
        self.gameClockDisplay.DisableClock()
        self.time.ResetTicksCounter()

    def StartNewRound(self):
        if (self.currentRoundIndex < 2):
            self.UpdatePreviousRound()
            self.currentRoundIndex += 1
            self.gameClockDisplay.EnableClock()
            self.BlueTeamScoreBoards[self.currentRoundIndex].EnableDisplay()
            self.RedTeamScoreBoards[self.currentRoundIndex].EnableDisplay()

    def ManageGameTime(self):
        self.time.UpdateTime()
        self.gameClockDisplay.UpdateClock(self.time.GetFormatedTime())
        if self.time.HasTimeExpired():
            self.gameClockDisplay.DisableClock()
            self.BlueTeamScoreBoards[self.currentRoundIndex].DisableDisplay()
            self.RedTeamScoreBoards[self.currentRoundIndex].DisableDisplay()
        else:
            self.UpdateScoreBoard()

    def UpdateScoreBoard(self):
        self.BlueTeamScoreBoards[self.currentRoundIndex].UpdateScore(self.RedTeam.GetScore())
        self.RedTeamScoreBoards[self.currentRoundIndex].UpdateScore(self.BlueTeam.GetScore())

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
    return 0

if __name__ == '__main__':
    sys.exit(main())