import random

oranges=2022
apples=1729
orangesLeft=oranges
applesLeft=apples
orangeWin=0
appleWin=0
for x in range(0, 100):
#    print(orangesLeft)
 #   print(applesLeft)
    while orangesLeft>1 and applesLeft>1:
        if random.uniform(0, 1)<=(orangesLeft*(orangesLeft-1))/((orangesLeft+applesLeft)*(orangesLeft+applesLeft-1)):
            orangesLeft-=2
            applesLeft+=1
        elif random.uniform(0, 1)<=(applesLeft*(applesLeft-1))/((orangesLeft+applesLeft)*(orangesLeft+applesLeft-1)):
            applesLeft-=1
        elif random.uniform(0, 1)<=(applesLeft*orangesLeft)/((orangesLeft+applesLeft)*(orangesLeft+applesLeft-1)):
            applesLeft-=1
    if applesLeft>orangesLeft:
        appleWin+=1
    else:
        orangeWin+=1
    applesLeft=apples
    orangesLeft=oranges
print(appleWin/(orangeWin+appleWin))