
import time

# we use this to make sense of the game state 
# I'm probably missing the point but that's okay
#
# positions will align the positions 
# return a dict
#  roll-> {gnubg.posinfo()["dice"]
#  cube -> {gnubg.posinfo()["cube"]
#  positions-> [myPositions, theirPositions] 
#           
def getGameState(rev):
   gameState = {}
   print str(gnubg.posinfo())
   gameState["dice"] = gnubg.posinfo()["dice"]
   gameState["doubled"] = gnubg.posinfo()["doubled"]
   gameState["resigned"] = gnubg.posinfo()["resigned"]
   board = gnubg.board()
   gameState["positions"] = []
   if(rev == 0):
      gameState["positions"].append(list(board[1]))
      gameState["positions"].append(list(reversed(board[0])))
   else:
      gameState["positions"].append(list(board[1]))
      gameState["positions"].append(list(reversed(board[0])))

   theirBar = gameState["positions"][1][0]
   gameState["positions"][1] = gameState["positions"][1][1:25]
   gameState["positions"][1].append(theirBar)
   return gameState

def maxIndex(positions):
   max = 0
   for i in range(0, len(positions)):
      if(positions[i] > 0):
         max = i
   return max

def bearoffable(positions):
   bear = True
   for i in range(6, 25):
      if(positions[i] > 0):
         bear = False
         break
   return bear

# we need to move
# second we consider whether we need to get off the bar 
def bgmove(state):
   # is there a resignation offer? 
   if(state["resigned"] >0):
      gnubg.command('accept')
      return

   # first, are we being doubled? 
   if(state["doubled"] == 1):
      gnubg.command('accept')
      return

   # is our move to roll? 
   dice = state["dice"]
   if(dice == (0, 0)):
      print "rolling"
      gnubg.command('roll')
      return 

   moves = []
   moves.extend(dice)
   # go double for doubles
   if(moves[0] == moves[1]):
      moves.extend(dice)

   myPositions = state["positions"][0]
   theirPositions = state["positions"][1]

   print "dice = " + str(dice)
   print "moves = " + str(moves)
   print "mP = " + str(myPositions)
   print "tP = " + str(theirPositions)
   print gnubg.posinfo()
   gnubg.command("show fullboard")

   # store the command here 
   command = []
   # we will find something for all 25s first 
   unusedMoves = []
   while(myPositions[24] > 0 and len(moves) > 0):
      for j in moves:
         if(theirPositions[24-j] <= 1 and myPositions[24] > 0):
            command.append("%d/%d" % (24+1, 24+1-j)) # remember to adjust index for 0 index array, 1 indexed board
            # adjust our positions to reflect move 
            myPositions[24] -= 1
            myPositions[24-j] += 1
            print "making move " + str(24+1) + "/" + str(j)
            moves.remove(j)
         else:
            moves.remove(j)
            unusedMoves.append(j)
   moves.extend(unusedMoves)

   # if myPositions[24] > 0 we can't move anymore
   if(myPositions[24] == 0):
      unusedMoves = []
      moved = False
      while(len(moves) > 0): 
         for j in moves:
            for i in reversed(range(0, 24)):
               if(myPositions[i] > 0):
                  print "considering position " + str(i+1) + " move " + str(j) + " with positions = " + str(myPositions)
                  # we need to check that we are able to bearoff exactly or that this is the furthest bearoffable piece

                  if(bearoffable(myPositions) and (i-j == -1 or (i-j < -1 and maxIndex(myPositions) == i))):
                     print "bearoff position = " + str(i+1)
                     command.append("%d/off" % (i+1))
                     myPositions[i] -= 1
                     moves.extend(unusedMoves)
                     unusedMoves = []
                     moved = True
                     break

                  if( (i-j >= 0) and (theirPositions[i-j] <= 1) ):
                     print "making move " + str(i+1) + "/" + str(j)
                     print "   theirPositions[i-j] = " + str(theirPositions[i-j])
                     command.append("%d/%d" % (i+1, i+1-j))
                     myPositions[i] -= 1
                     myPositions[i-j] += 1
                     moves.extend(unusedMoves)
                     unusedMoves = []
                     moved = True
                     break # j 
            print "remove move = " + str(j)
            moves.remove(j)
            if(moved == False):
               unusedMoves.append(j)
            moved = False
            break
         # if we made one move we need to consider the removed moves again

   commandString = ""
   for c in command:
      commandString += c
      commandString += " "
   print "command = " + commandString
   gnubg.command(commandString)




gnubg.command('set player 0 chequer evaluation plies 0')
gnubg.command('set player 0 chequer evaluation prune off')
gnubg.command('set player 0 chequer evaluation noise 0.060')
gnubg.command('set automatic game off')
gnubg.command('set jacoby off')
gnubg.command('set delay 0')
gnubg.command('set automatic move on')
gnubg.command('save settings')

def playMatch():
   gnubg.command('new match 1')
   pos = gnubg.posinfo()
   print "position"
   print gnubg.posinfo()
   print gnubg.posinfo()["dice"]
   rev = 0
   if(gnubg.posinfo()["dice"] == (0, 0)):
      print "you need to roll"
      gnubg.command('roll')
      rev = 1
   else:
      print "you won the roll"
      rev = 0
   print "rev = " + str(rev)
   dice = gnubg.posinfo()["dice"]
   print "dice: "
   print dice
   board = gnubg.board()

   same = 0
   lastBoard = []
   while(same < 3 and gnubg.match()["games"][0]["info"]["winner"] == None):
      print "turn!"
      print gnubg.posinfo()
      state = getGameState(rev)
      if(same > 0):
         state["dice"] = reversed(state["dice"])
      bgmove(state)
      state = getGameState(rev)
      if(lastBoard == state["positions"]):
         same += 1
      else:
         same = 0
      lastBoard = state["positions"]
      print state["positions"][0]
      print state["positions"][1]
      print gnubg.posinfo()
   winner = str(gnubg.match()["games"][0]["info"]["winner"])
   print "winner = " + winner
   print gnubg.match()["games"][0]["info"]
   if(winner == "O"):
      return gnubg.match()["games"][0]["info"]["points-won"]
   elif(winner == "X"):
      return -gnubg.match()["games"][0]["info"]["points-won"]
   return 0


myPoints = 0
theirPoints = 0
badPoints = 0

while(myPoints < 10000 and theirPoints < 10000):
   point = playMatch()
   if(point > 0):
      myPoints += point
   elif(point < 0): 
      theirPoints -= point 
   else:
      badPoints += 1
   avg=0
   avgBad = 0
   if(myPoints + theirPoints > 0):
      avg = myPoints / float(myPoints + theirPoints)
      avgBad = badPoints / float(myPoints + theirPoints + badPoints)
   print "Current Score: me = " + str(myPoints) + " them = " + str(theirPoints) + " bad games = " + str(badPoints) + " (" + str(avg) + ") bad = (" + str(avgBad) + ")"




