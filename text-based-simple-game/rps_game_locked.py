'''
    Name:           rock_paper_scissors.py
    Purpose:        To improve Python skills
    Author:         Neeraj
    Date;Time:      1st October, 2018; 23:45 hrs
    Passkey:        'Neeraj224'
'''
#   NOTE:   Want to add asynchronous skip-intro method
#   NOTE:   Too many sleep() calls - always a bad idea

import sys      # for sys()
import os       # for system("clear")
import vlc      # for in-game tunes
import random   # to use the random number generator provided by python
import time     # to utilise the nobility that is sleep()
import datetime # to get the current date and time
import psutil   # to get system status
import getpass  # to get the password input in ciphertext
from termcolor import colored, cprint   #   for blinking text!
#from multiprocessing import Pool    #   to use threads for skipping intro


#   A try at the simple implementation of thec rock-paper-scissor game
#   I will try to implement what I've learnt

#   ------------------- This is a little game of rock-paper-scissors I've tried to hack away
#   ------------------- at. It's pretty clanky. It was made solely for the purpose of learning
#   ------------------- and improving my Python skills. Please feel free to modify or distribute
#   ------------------- the source code. And last but not the least, enjoy!

#   pre-defined values for the entities of the game
'''

    RULES:
        Rock beats scissors; scissors beats paper(obviously);
        and paper beats rock.

'''
#   --------------------------------- User-defined functions ---------------------------------
#   Colors: There are 8 colors - ANSI codes 30 to 37
#   31 - red
#   32 - green
#   33 - yellow
#   34 - violet
#   35 - pink
#   36 - blue
#   37 - white
#   function to color terminal text:
#   params - this_color gives the color code from any of the above, and string holds the string that is to be colored
def color(this_color, string):
    #   the "1;" makes the entire string colored, bold. to make it regular, remove the "1;"!
    return "\033[" + "1;" +this_color + "m" + string + "\033[0m"

#   The follwing function clears the screen and places the cursor position to the top left corner of the stdout(i.e., terminal)
def clear():
    """Clear screen, return cursor to top left"""
    #   the following write a pair of ANSI escape sequences to clear the screen!!
    sys.stdout.write('\033[2J')
    sys.stdout.write('\033[H')
    sys.stdout.flush()

def dev_mode_stats():
    clear()
    time.sleep(2)
    print(color(str(36), "Entering in developer-mode."))
    time.sleep(1)
    print(color(str(36), "Date and time: " + str(datetime.datetime.now())))
    time.sleep(0.5)
    print(color(str(34), "Virtual Memory:\n" + str(psutil.virtual_memory())))
    time.sleep(0.5)
    print(color(str(31), "CPU Frequency:\n" + str(psutil.cpu_freq())))
    time.sleep(0.5)
    print(color(str(34), "CPU Count: " + str(psutil.cpu_count())))
    time.sleep(0.5)
    print(color(str(35), "CPU Statistics:\n" + str(psutil.cpu_stats())))
    time.sleep(1)
    print(color(str(35), "CPU Times: " + str(psutil.cpu_times())))
    time.sleep(1)

#   --------------------------------- List Ends ---------------------------------

#   Some important variables that we'll need:
CANCEL_FLAG = False     # to be used to continue the game if the player enters wrong input
TIE_FLAG = False        # to be used to calculate the points
POINTS_PLAYER = 0       # to be used to calculate the points for the player
POINTS_COMPUTER = 0     # to be used to calculate the points for the computer
BATTLE_TUNE = False     # used for tuning the music at the right time
SKIP_INTRO_FLAG = False # used to check if the intro was skipped

rock = 1
paper = 2
scissor = 3

#   tags to check if the player is the winner or the computer(?)
player_win = False
computer_win = False

#   whose turn is it to play?
#   1 -> means it's turn to play (whoever needs to )
#   0 -> means it has played
player_turn = 0
computer_turn = 0

#   what did the computer play?
computer_play = 0
#   what did the player play?
player_play = 0

# check dev_mode_stats()
dev_mode_stats()

clear()

#   Password protection for developer mode:
while 1:
    print(color(str(37), "Enter the"), color(str(34), "pass-key"), ":")
    pass_key = getpass.getpass()	#	to encrypt the password in ciphertext, so no one sees it while we enter it
    if pass_key == "Neeraj224":
        clear()
        break
    else:
        clear()
        print(color(str(37), "Wrong key entered."))
        continue

#   ASCII art made using text-to-ascii-generator:
battle_text1 = """\
 
 █     █░▓█████  ██▓     ▄████▄   ▒█████   ███▄ ▄███▓▓█████    ▄▄▄█████▓ ▒█████  
▓█░ █ ░█░▓█   ▀ ▓██▒    ▒██▀ ▀█  ▒██▒  ██▒▓██▒▀█▀ ██▒▓█   ▀    ▓  ██▒ ▓▒▒██▒  ██▒
▒█░ █ ░█ ▒███   ▒██░    ▒▓█    ▄ ▒██░  ██▒▓██    ▓██░▒███      ▒ ▓██░ ▒░▒██░  ██▒
░█░ █ ░█ ▒▓█  ▄ ▒██░    ▒▓▓▄ ▄██▒▒██   ██░▒██    ▒██ ▒▓█  ▄    ░ ▓██▓ ░ ▒██   ██░
░░██▒██▓ ░▒████▒░██████▒▒ ▓███▀ ░░ ████▓▒░▒██▒   ░██▒░▒████▒     ▒██▒ ░ ░ ████▓▒░
░ ▓░▒ ▒  ░░ ▒░ ░░ ▒░▓  ░░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ░  ░░░ ▒░ ░     ▒ ░░   ░ ▒░▒░▒░ 
  ▒ ░ ░   ░ ░  ░░ ░ ▒  ░  ░  ▒     ░ ▒ ▒░ ░  ░      ░ ░ ░  ░       ░      ░ ▒ ▒░ 
  ░   ░     ░     ░ ░   ░        ░ ░ ░ ▒  ░      ░      ░        ░      ░ ░ ░ ▒  
    ░       ░  ░    ░  ░░ ░          ░ ░         ░      ░  ░                ░ ░  
                        ░                                                        
                                                                                     
"""

battle_text2 = """\

▓██   ██▓ ▒█████   █    ██  ██▀███     ▓█████▄  ▒█████   ▒█████   ███▄ ▄███▓ ▐██▌ 
 ▒██  ██▒▒██▒  ██▒ ██  ▓██▒▓██ ▒ ██▒   ▒██▀ ██▌▒██▒  ██▒▒██▒  ██▒▓██▒▀█▀ ██▒ ▐██▌ 
  ▒██ ██░▒██░  ██▒▓██  ▒██░▓██ ░▄█ ▒   ░██   █▌▒██░  ██▒▒██░  ██▒▓██    ▓██░ ▐██▌ 
  ░ ▐██▓░▒██   ██░▓▓█  ░██░▒██▀▀█▄     ░▓█▄   ▌▒██   ██░▒██   ██░▒██    ▒██  ▓██▒ 
  ░ ██▒▓░░ ████▓▒░▒▒█████▓ ░██▓ ▒██▒   ░▒████▓ ░ ████▓▒░░ ████▓▒░▒██▒   ░██▒ ▒▄▄  
   ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░    ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░   ░  ░ ░▀▀▒ 
 ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░   ░▒ ░ ▒░    ░ ▒  ▒   ░ ▒ ▒░   ░ ▒ ▒░ ░  ░      ░ ░  ░ 
 ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░   ░░   ░     ░ ░  ░ ░ ░ ░ ▒  ░ ░ ░ ▒  ░      ░       ░ 
 ░ ░         ░ ░     ░        ░           ░        ░ ░      ░ ░         ░    ░    
 ░ ░                                    ░                                         
                                                                        
"""

#   start playing the tune
narration_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/narration_tune.mp3")
narration_tune.play()
time.sleep(10)  # I think it's important to call sleep() after playing a tune(?)

clear()
#   by using the color() function, we are coloring the strings - in the terminal
#   using yellow color(33) for acronyms and red color(31) to address the player
print("\n\n\t\t", color(str(37), "Welcome to"), color(str(32), "The Game."), "\n\t\t", color(str(37), "Prepare to bow under the reign of Singularity."))
time.sleep(3)

print("\t\t", color(str(37), "The story so far..."))
time.sleep(2)
print("\t\t", color(str(37), "Humanity\'s directing and foremost think-tank, VDGine Laboratories,"))
time.sleep(2)
print("\t\t", color(str(37), "has contrived up a machine called"))
time.sleep(2)
print("\t\t", color(str(33), "the B.O.T.- Machine (short for Barely Organic Turing - Machine)."))
time.sleep(2)
print("\t\t", color(str(37), "VDGine's dissenting opponents, the ecclesiastical group of"))
time.sleep(2)
print("\t\t", color(str(33), "O.A.F.S.(Opposing Antagonistic & Faithful Saints)"))
time.sleep(2)
print("\t\t", color(str(37), "has released a cataclysmic virus named,"))
time.sleep(2)
print("\t\t", color(str(33), "N.E.L.L.(Neurogenic Evil Lethargic Lab-rat)"), color(str(37), "to erase"))
time.sleep(2)
print("\t\t", color(str(33), "the B.O.T.- Machine."), color(str(37), "But because of its laziness,"))
time.sleep(2)
print("\t\t", color(str(33), "N.E.L.L."), color(str(37), "has ended up cutting its work by simply corrupting"))
time.sleep(2)
print("\t\t", color(str(37), "the Machine."), color(str(33), "The B.O.T.- Machine (now calling itself"))
time.sleep(2)
print("\t\t", color(str(33), "the \"Bitterly Outraged and Troubled - Machine\")"))
time.sleep(2)
print("\t\t", color(str(37), "has vowed to end humanity."))
time.sleep(5)
print("\t\t", color(str(37), "It is up to"), color(str(31), "YOU"), color(str(37), "now"), color(str(31), "O unrelated and unconcerned stranger,"))
time.sleep(2)
print("\t\t", color(str(37), "to liberate mankind from the so-so evil clutches"))
time.sleep(2)
print("\t\t", color(str(37), "of"), color(str(33), "the B.O.T.- Machine."), color(str(31), "YOU"), color(str(37), "have challenged it in"))
time.sleep(5)
print("\n\n\t\t", color(str(31), "AN ANCIENT AND DEADLY GAME!"))
time.sleep(2)
print("\t\t", color(str(31), "Prepare for battle!"))

print(color(str(37), "Please enter your name:"))
name = input()

narration_tune.stop()

computer_turn = 1

#   doom_tune first!
clear()
doom_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/doom_tune.mp3")
doom_tune.play()

#   begin blinking text!!!
cprint("\n\n\n\n\n\t\t" + color(str(31), battle_text1), attrs = ['blink'])
cprint("\n\n\n\t\t" + color(str(31), battle_text2), attrs = ['blink'])

#   let the doom tune play for a few seconds!
time.sleep(15)
doom_tune.stop()

battle_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/battle_tune.mp3")

clear() #   warmup call to clear!

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
        print("\n" + name + ", ", color(str(37), "enter your hand (Please enter either \'rock\', \'paper\' or \'scissor\'):"))
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
        print("", color(str(37), "Wrong hand played.\nPlease try again."))
        CANCEL_FLAG = True  # can i comment it?
        continue

        time.sleep(1)
    # main logic of the game:
    if computer_play == player_play:
        print("\n" + color(str(37), "It's a tie.\nNobody wins a point"))
        TIE_FLAG = True
    elif computer_play == scissor and player_play == paper:
        print("\n" + color(str(31), "B.O.T.") + color(str(37), " played scissor and ") + color(str(34), name) + color(str(37), " played paper!\n") + color(str(31), "B.O.T.") + color(str(37), " scores a point!"))
        POINTS_COMPUTER += 1
    elif computer_play == scissor and player_play == rock:
        print("\n" + color(str(31), "B.O.T.") + color(str(37), " played scissor and ") + color(str(34), name) + color(str(37), " played rock!\n") + color(str(34), name) + color(str(37), " scores a point!"))
        POINTS_PLAYER += 1
    elif computer_play == paper and player_play == rock:
        print("\n" + color(str(31), "B.O.T.") + color(str(37), " played paper and ") + color(str(34), name) + color(str(37), " played rock!\n") + color(str(31), "B.O.T. ") + color(str(37), "scores a point!"))
        POINTS_COMPUTER += 1
    elif computer_play == paper and player_play == scissor:
        print("\n" + color(str(31), "B.O.T. ") + color(str(37), "played paper and ") + color(str(34), name) + color(str(37), " played scissor!\n") + color(str(34), name) + color(str(37), " scores a point!"))
        POINTS_PLAYER += 1
    elif computer_play == rock and player_play == scissor:
        print("\n" + color(str(31), "B.O.T. ") + color(str(37), "played rock and ") + color(str(34), name) + color(str(37), " played scissor!\n"), color(str(31), "B.O.T. ") + color(str(37), "scores a point!"))
        POINTS_COMPUTER += 1
    elif computer_play == rock and player_play == paper:
        print("\n" + color(str(31), "B.O.T. ") + color(str(37), "played rock and ") + color(str(34), name) + color(str(37), " played paper!\n") + color(str(34), name) + color(str(37), " scores a point!"))
        POINTS_PLAYER += 1

        time.sleep(1)
    # display the scoreboard:
    print("\n\n\t\t" + color(str(37), "Scoreboard:"))
    print("\t\t" + color(str(34), name) + color(str(37), " points:"), POINTS_PLAYER)
    print("\t\t" + color(str(31), "B.O.T.") + color(str(37), " points:"), POINTS_COMPUTER)

    time.sleep(2)   # called, so that the clear() doesn't clear the screen too fast
    clear()

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

battle_tune.stop()

dead_text = """\


▓██   ██▓ ▒█████   █    ██     ▄▄▄       ██▀███  ▓█████    ▓█████▄ ▓█████ ▄▄▄      ▓█████▄      
 ▒██  ██▒▒██▒  ██▒ ██  ▓██▒   ▒████▄    ▓██ ▒ ██▒▓█   ▀    ▒██▀ ██▌▓█   ▀▒████▄    ▒██▀ ██▌     
  ▒██ ██░▒██░  ██▒▓██  ▒██░   ▒██  ▀█▄  ▓██ ░▄█ ▒▒███      ░██   █▌▒███  ▒██  ▀█▄  ░██   █▌     
  ░ ▐██▓░▒██   ██░▓▓█  ░██░   ░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄    ░▓█▄   ▌▒▓█  ▄░██▄▄▄▄██ ░▓█▄   ▌     
  ░ ██▒▓░░ ████▓▒░▒▒█████▓     ▓█   ▓██▒░██▓ ▒██▒░▒████▒   ░▒████▓ ░▒████▒▓█   ▓██▒░▒████▓  ██▓ 
   ██▒▒▒ ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒     ▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░    ▒▒▓  ▒ ░░ ▒░ ░▒▒   ▓▒█░ ▒▒▓  ▒  ▒▓▒ 
 ▓██ ░▒░   ░ ▒ ▒░ ░░▒░ ░ ░      ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░    ░ ▒  ▒  ░ ░  ░ ▒   ▒▒ ░ ░ ▒  ▒  ░▒  
 ▒ ▒ ░░  ░ ░ ░ ▒   ░░░ ░ ░      ░   ▒     ░░   ░    ░       ░ ░  ░    ░    ░   ▒    ░ ░  ░  ░   
 ░ ░         ░ ░     ░              ░  ░   ░        ░  ░      ░       ░  ░     ░  ░   ░      ░  
 ░ ░                                                        ░                       ░        ░  


"""

win_text = """\


▄██   ▄    ▄██████▄  ███    █▄        ▄█     █▄   ▄██████▄  ███▄▄▄▄   
███   ██▄ ███    ███ ███    ███      ███     ███ ███    ███ ███▀▀▀██▄ 
███▄▄▄███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
▀▀▀▀▀▀███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
▄██   ███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
███   ███ ███    ███ ███    ███      ███     ███ ███    ███ ███   ███ 
███   ███ ███    ███ ███    ███      ███ ▄█▄ ███ ███    ███ ███   ███ 
 ▀█████▀   ▀██████▀  ████████▀        ▀███▀███▀   ▀██████▀   ▀█   █▀  
                                                                      


"""

goddangit_text = """\


   ▄██████▄   ▄██████▄  ████████▄  ████████▄     ▄████████ ███▄▄▄▄      ▄██████▄   ▄█      ███     
  ███    ███ ███    ███ ███   ▀███ ███   ▀███   ███    ███ ███▀▀▀██▄   ███    ███ ███  ▀█████████▄ 
  ███    █▀  ███    ███ ███    ███ ███    ███   ███    ███ ███   ███   ███    █▀  ███▌    ▀███▀▀██ 
 ▄███        ███    ███ ███    ███ ███    ███   ███    ███ ███   ███  ▄███        ███▌     ███   ▀ 
▀▀███ ████▄  ███    ███ ███    ███ ███    ███ ▀███████████ ███   ███ ▀▀███ ████▄  ███▌     ███     
  ███    ███ ███    ███ ███    ███ ███    ███   ███    ███ ███   ███   ███    ███ ███      ███     
  ███    ███ ███    ███ ███   ▄███ ███   ▄███   ███    ███ ███   ███   ███    ███ ███      ███     
  ████████▀   ▀██████▀  ████████▀  ████████▀    ███    █▀   ▀█   █▀    ████████▀  █▀      ▄████▀   
                                                                                                   


"""

bot_text1 = """\

██╗  ██╗ ██████╗ ████████╗    ██████╗ ██╗ ██████╗  ██████╗ ██╗████████╗██╗   ██╗
██║  ██║██╔═══██╗╚══██╔══╝    ██╔══██╗██║██╔════╝ ██╔════╝ ██║╚══██╔══╝╚██╗ ██╔╝
███████║██║   ██║   ██║       ██║  ██║██║██║  ███╗██║  ███╗██║   ██║    ╚████╔╝ 
██╔══██║██║   ██║   ██║       ██║  ██║██║██║   ██║██║   ██║██║   ██║     ╚██╔╝  
██║  ██║╚██████╔╝   ██║       ██████╔╝██║╚██████╔╝╚██████╔╝██║   ██║      ██║▄█╗
╚═╝  ╚═╝ ╚═════╝    ╚═╝       ╚═════╝ ╚═╝ ╚═════╝  ╚═════╝ ╚═╝   ╚═╝      ╚═╝╚═╝

                                                                                                                                                                                           
"""

bot_text2 = """\

██╗    ██╗    ██╗ ██████╗ ███╗   ██╗██╗
██║    ██║    ██║██╔═══██╗████╗  ██║██║
██║    ██║ █╗ ██║██║   ██║██╔██╗ ██║██║
██║    ██║███╗██║██║   ██║██║╚██╗██║╚═╝
██║    ╚███╔███╔╝╚██████╔╝██║ ╚████║██╗
╚═╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝
                                       

"""

coin_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/coin_tune.mp3")
coin_tune.play()
time.sleep(1)
coin_tune.stop()

if computer_win is True:
    bot_win_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/bot_win.mp3")
    bot_win_tune.play()
    clear()
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\t\t", color(str(31), "The B.O.T.- Machine"), color(str(37), "won the game and showed everyone what it is capable of!"))
    time.sleep(2)
    clear()
    time.sleep(2)
    cprint("\n\n\n\n\t\t" + color(str(33), bot_text1), attrs = ['blink'])
    cprint("\n\n\n\n\t\t" + color(str(33), bot_text2), attrs = ['blink'])
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\t\t", color(str(34), "You"), color(str(37), "have failed humankind miserably."))
    clear()
    time.sleep(2)
    cprint("\n\n\n\n\t\t" + color(str(31), dead_text), attrs = ['blink'])
    time.sleep(5)
    bot_win_tune.stop()
else:
    player_win_tune = vlc.MediaPlayer("/Users/neeraj/Desktop/Codes/_other_languages/Python/text-based-simple-game/tunes/player_win_tune.mp3")
    player_win_tune.play()
    clear()
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\t\t", color(str(31), name), color(str(37), "has successfully strived to rise above the machine this time and win."))
    time.sleep(2)
    clear()
    cprint("\n\n\n\n\n\t\t" + color(str(33), goddangit_text), attrs = ['blink'])
    time.sleep(2)
    clear()
    cprint("\n\n\n\n\t\t" + color(str(33), win_text), attrs = ['blink'])
    time.sleep(2)
    print("\n\n\n\n\n\n\n\n\n\t\t", color(str(37), "But can"), color(str(34), name), color(str(37), "win again...?"))
    time.sleep(5)
    player_win_tune.stop()

time.sleep(3)

clear() #   last call to clear(), so that after the game ends, the cursor position is back to normal

