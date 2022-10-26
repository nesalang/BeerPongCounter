from guizero import App, Text
class ClockLabel:
    def __init__(self, app, timeString, clockEventHandler):
        self.clockTickCounter = ClockTicksCounter(time)
        self.clock = Text(app, text = self.clockTickCounter.GetFormatedTime(), size=70, font = 'Times New Roman', width = 'fill', align = 'top')
        self.clock = Text(app, text = timeString, size=70, font = 'Times New Roman', width = 'fill', align = 'top')
        self.clock.repeat(1000, self.UpdateClockDisplay)
        self.clockEventHandler = clockEventHandler

    def UpdateClockDisplay(self):
        self.clock.value = self.clockTickCounter.GetUpdatedTime()
        self.clockEventHandler();

    def ResetClock(self):
        self.clockTickCounter.ResetTicksCounter()

class ScoreLabels:
    def __init__(self, app, color, alignment, scoreEventHandler):
        #self.padding = Text(app, text='   ', size=70, font ="Times New Roman", align=alignment)
        self.score = Text(app, text=1, size=70, font ="Times New Roman", color= color, align=alignment)
        self.scoreEventHandler = scoreEventHandler
        self.RegisterCallBack()

    def ResetScore(self):
        self.score.value = 0

    def UpdateScore(self, score):
        self.score.value = score

    def RegisterCallBack(self):
        self.score.repeat(1000, self.scoreEventHandler)
         
class ScoreLabelsLeft(ScoreLabels):
    def __init__(self, app):
        super().__init__(app, 'blue', 'left')


class ScoreLabelsRight(ScoreLabels):
    def __init__(self, app):
        super().__init__(app, 'red', 'right')

class ClockTicksCounter:
    def __init__(self, time):
        self.time = time
        self.ResetTicksCounter()

    def ResetTicksCounter(self):
        self.seconds = time * 60

    def UpdateTime(self):
        if self.seconds > 0:
            self.seconds -= 1

    def HasTimeExpired(self):
        return self.seconds <= 0
            
    def GetFormatedTime(self):
        mininutes = self.seconds // 60
        seconds = self.seconds % 60
        secondsInString = str(seconds) if seconds != 0 else '00'
        timeString = str(mininutes) + ' : ' + secondsInString if mininutes else secondsInString
        print(timeString)
        return timeString

    def GetUpdatedTime(self):
        self.UpdateTime()
        return self.GetFormatedTime()

class ScoreSource:
    def __init__(self):
        self.count = 0

    def GetScore(self):
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

    def __iter__(self):
        self.teamIndex = 0
        return self

    def __next__(self):
        if self.teamIndex < len(self.team):
            team = self.teams[self.teamIndex]
            self.teamIndex + 1;
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
            for team in self.teams.values():
                team.UpdateScore()

    def IsGameOver(self):
        return self.gameClock.HasTimeExpired()

class Game:
    def __init__(self, time, rounds):
        self.time = time
        self.numberOfRounds = rounds
        self.currentRoundIndex = 0
        self.rounds = [Round(Team("Red"), Team("Blue"), ClockTicksCounter(time)) for _ in range(rounds)]
        self.hasNewRoundStarted = False
        self.app = App(title="Welcome To Pong Game!!!")
        self.redTeamScore = ScoreLabelsRight(app, self.UpdateScoreBoard)
        self.blueTeamScore = ScoreLabelsLeft(app, self.UpdateScoreBoard)
        self.gameClock = ClockLabel(app, 5, self.ManageGameTime)
        self.teams = { "Red" : self.redTeamScore, "Blue" : self.blueTeamScore };
        self.app.display()

    def ResetUI(self):
        self.redTeamScore.ResetScore()
        self.blueTeamScore.ResetScore()
        self.gameClock.ResetClock()

    def StartNewRound(self):
        if self.currentRoundIndex < len(self.rounds) - 1:
            self.currentRoundIndex += 1
            self.ResetUI()
            self.hasNewRoundStarted = True

    def ManageGameTime(self):
        if self.hasNewRoundStarted == False:
            return
        #Update UI
        currentRound = self.rounds[self.currentRoundIndex]
        currentRound.UpdateGameTime()
        if currentRound.IsGameOver():
            winningTeam = currentRound.GetWinner()
            self.hasNewRoundStarted = False
            # Update UI:w

    def UpdateScoreBoard(self):
        currentRound = self.rounds[self.currentRoundIndex]
        if not currentRound.IsGameOver():
            for eachTeam in currentRound:
                # get score label and update the score
                self.teams[eachTeam.GetTeamName()].UpdateScore(eachTeam.GetScore())

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
        


app = App(title="Hello World")
redTeamScore = ScoreLabelsRight(app)
blueTeamScore = ScoreLabelsLeft(app)
gameClock = ClockLabel(app, 5)

app.display() 
                            
