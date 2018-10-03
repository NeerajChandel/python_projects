'''
    Name:           rock_paper_scissors.py
    Purpose:        To improve Python skills
    Author:         Neeraj
    Date;Time:      1st October, 2018; 23:45 hrs
'''
import vlc      # for in-game tunes
import random   # to use the random number generator provided by python
import time     # to use sleep(secs) function for waiting time

#   A try at the simple implementation of the rock-paper-scissor game
#   I will try to implement what I've learnt

#   ------------------- This is a little game of rock-paper-scissors I've tried to hack away
#   ------------------- at. It's pretty clanky. It was made solely for the purpose of learning
#   ------------------- and improving my Python skills. Please feel free to modify or distribute
#   ------------------- the spurce code. And last but not the least, enjoy!

#   pre-defined values for the entities of the game
'''

    RULES:
        Rock beats scissors; scissors beats paper(obviously);
        and paper beats rock.
        So, 1 beats 3; 3 beats 2; 2 beats 1

'''

#   Some important variables that we'll need:
CANCEL_FLAG = False     # to be used to continue the game if the player enters wrong input
TIE_FLAG = False        # to be used to calculate the points
POINTS_PLAYER = 0       # to be used to calculate the points for the player
POINTS_COMPUTER = 0     # to be used to calculate the points for the computer
BATTLE_TUNE = False       # used for the tuning the music

rock = 1
paper = 2
scissor = 3

#   tags to check if the player is the winner or the computer
player_win = False
computer_win = False

#   whose turn is it to play?
#   1 -> means it's turn to play
#   0 -> means it has played
player_turn = 0
computer_turn = 0

#   what did the computer play?
computer_play = 0
#   what did the player play?
player_play = 0

narration_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/narration_tune.mp3")
narration_tune.play()
time.sleep(10)  # I think it's important to call sleep() after playing a tune(?)

print("\n\n\t\tWelcome to The Game\n\t\tPrepare to bow under the reign of Singularity.")
time.sleep(5)
print("\t\tThe story so far...")
time.sleep(2)
print("\t\tHumanity\'s directing and foremost think-tank, VDGine Laboratories,")
time.sleep(2)
print("\t\thas contrived up a machine called")
time.sleep(2)
print("\t\tthe B.O.T.- Machine (short for Barely Organic Turing - Machine).")
time.sleep(2)
print("\t\tVDGine's dissenting opponents, the ecclesiastical group of")
time.sleep(2)
print("\t\tO.A.F.S.(Opposing Antagonistic & Faithful Saints)")
time.sleep(2)
print("\t\thas released a cataclysmic virus named,")
time.sleep(2)
print("\t\tN.E.L.L.(Neurogenic Evil Lethargic Lab-rat), to erase")
time.sleep(2)
print("\t\tthe B.O.T.- Machine. But because of its laziness,")
time.sleep(2)
print("\t\tN.E.L.L. has ended up cutting its work by simply corrupting")
time.sleep(2)
print("\t\tthe Machine. The B.O.T.- Machine (now calling itself")
time.sleep(2)
print("\t\tthe \"Bitterly Outraged and Troubled - Machine\")")
time.sleep(2)
print("\t\thas vowed to end humanity.")
time.sleep(5)
print("\t\tIt is up to you now, O unrelated and unconcerned stranger,")
time.sleep(2)
print("\t\tto liberate mankind from the so-so evil clutches")
time.sleep(2)
print("\t\tof the B.O.T.- Machine. You have challenged it in")
time.sleep(5)
print("\n\n\t\tAN ANCIENT AND DEADLY GAME OF ROCK-PAPER-SCISSORS!")
time.sleep(2)
print("\t\tPrepare for battle!")

narration_tune.stop()

computer_turn = 1

battle_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/battle_tune.mp3")

#   A main game loop that checks whether anyone won or not; if someone wins,
#   it's flag is set inside, and the condition tested for the while loop
#   turns false, which breaks the loop. Another
while computer_win is False or player_win is False or CANCEL_FLAG is False:
    if BATTLE_TUNE is False:
        battle_tune.play()
        #time.sleep(1)
    else:
        battle_tune.stop()
    # rand_var is used to decide the play of the computer:
    rand_var = random.randrange(0, 100)    # to make the game easy, change 1000 to 100!

    # check if the player has played(0) and if its the computer's turn to play(1)
    if player_turn == 0 and computer_turn == 1: # 1 means its the player's turn to play!
        # computer plays rock for the following conditions:
        if rand_var % 2 == 0 or rand_var % 4 == 0 or rand_var % 6 == 0 or rand_var % 8 == 0:
            computer_play = rock
            computer_turn = 0   # 0 means the computer has played
            player_turn = 1     # set it so that its the player's turn to play the next time

        # computer plays paper for the following conditions:
        elif rand_var % 3 == 0 or rand_var % 9 == 0 or rand_var % 5 == 0 or rand_var % 7 == 0:
            computer_play = paper
            computer_turn = 0
            player_turn = 1

        # if none of the conditions in the above checks is satisfied, the computer plays scissor
        else:
            computer_play = scissor
            computer_turn = 0
            player_turn = 1

    #   if the computer has played(0) and its the player's turn(1), then get input from the player
    if computer_turn == 0 and player_turn == 1:    # the computer has played, it's the player's turn
        print("\nPlayer, enter your hand (Please enter either \'rock\', \'paper\' or \'scissor\'):")
        player_play = input()
        player_turn = 0
        computer_turn = 1

    # check what the player played, and set the player_play variable accordingly!
    if player_play == "rock":
        player_play = rock
        CANCEL_FLAG = False
    elif player_play == "paper":
        player_play = paper
        CANCEL_FLAG = False
    elif player_play == "scissor":
        player_play = scissor
        CANCEL_FLAG = False
    # if the player types in anything other than 'rock', 'paper' or 'scissor', then continue to the loop!
    else:
        print("Wrong hand played.\nPlease try again.")
        CANCEL_FLAG = True  # can i comment it?
        continue

    # main logic of the game:
    if computer_play == player_play:
        print("\nIt's a tie.\nNobody wins a point")
        TIE_FLAG = True
    elif computer_play == scissor and player_play == paper:
        print("\nB.O.T. played scissor and the player played paper!\nB.O.T. scores a point!")
        POINTS_COMPUTER += 1
    elif computer_play == scissor and player_play == rock:
        print("\nB.O.T. played scissor and the player played rock!\nPlayer scores a point!")
        POINTS_PLAYER += 1
    elif computer_play == paper and player_play == rock:
        print("\nB.O.T. played paper and the player played rock!\nB.O.T. scores a point!")
        POINTS_COMPUTER += 1
    elif computer_play == paper and player_play == scissor:
        print("\nB.O.T. played paper and the player played scissor!\nPlayer scores a point!")
        POINTS_PLAYER += 1
    elif computer_play == rock and player_play == scissor:
        print("\nB.O.T. played rock and the player played scissor!\nB.O.T. scores a point!")
        POINTS_COMPUTER += 1
    elif computer_play == rock and player_play == paper:
        print("\nB.O.T. played rock and the player played paper!\nPlayer scores a point!")
        POINTS_PLAYER += 1

    # display the scoreboard:
    print("\n\n\t\tScoreboard:")
    print("\t\tPlayer points:", POINTS_PLAYER)
    print("\t\tB.O.T. points:", POINTS_COMPUTER)

    if POINTS_COMPUTER == 3:
        computer_win = True
        BATTLE_TUNE = True
        break
    elif POINTS_PLAYER == 3:
        player_win = True
        BATTLE_TUNE = True
        break
    else:
        continue

coin_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/coin_tune.mp3")
coin_tune.play()
time.sleep(3)

if computer_win is True:
    time.sleep(0.5)
    print("\n\n\t\tThe B.O.T.- Machine won the game and showed everyone what it is capable of!")
    time.sleep(2)
    print("\t\tYou have failed humankind miserably.")
else:
    time.sleep(0.5)
    print("\n\n\t\tThe player has successfully strived to rise above the machine this time and win.")
    time.sleep(2)
    print("\t\tBut can the player win again...?")

coin_tune.stop()
