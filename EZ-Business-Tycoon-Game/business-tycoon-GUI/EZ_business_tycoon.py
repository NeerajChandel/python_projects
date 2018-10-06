#   Purpose: Creating a Business Tycoon game (idle clicker) while learning
#            the basics object-oriented programming in Python.
#   Note: The game will have a pretty basic GUI.
#   Day/Date: Saturday/6th October 2018
#   Author: Neeraj

#   NOTE: while inserting data in csv file, do not put a space before the .gif files!

from tkinter import ttk
import time # for timer purposes
import tkinter as tk
import csv  # to read/manipulate csv files
from tkinter import *
from tkinter import messagebox

MONEY_FORMAT = '${:0,.2f}'  # if we wanna change it, we can simply do it here, not inside the code!
DIVIDER = "==================================================="
data_file = 'data.csv'
padding = 20    # to padx labels by 10
window_size = "1020x600" # passing it below to root_window.geometry(); it's easier to change it here though

#   The timer implemented requires us to use threads, and manage states (like a state machine)
#   to remember when the timer's running or when it's not running
class StoreTimer():
    update_freq = 100    # 100 milliseconds

    def __init__(self, store): # we'll pass along the store that the timer's (instance) is associated with
        self.timer = store.timer
        self.store = store # store the reference of the passed store
        self.timer_running = False  # for checking the state of the timer
        #self.start_timer()  # this is an important call! -> now we don't want to start timer in init(), we'll start it when we need it

    def start_timer(self):
        if self.timer_running == False:
            self.timer_running = True   # after turning the timer on, set the timer_running flag to True
            self.start_time = time.time()
            root_window.after(StoreTimer.update_freq, self.update_timer) # root -> this timer has to run off the root thread

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        if elapsed_time < self.timer:
            # update the progress bar by the elapsed time that we have by the total time given for the timer times 100:
            self.store.progress_bar["value"] = elapsed_time / self.timer * 100
            root_window.after(StoreTimer.update_freq, self.update_timer)
        else:
            # set the timer_running flag to False, as elapsed time finishes:
            self.timer_running = False
            # set the progress bar to zero after the timer is completed, and then make money!
            self.store.progress_bar["value"] = 0
            # now, when the timer stops, we want to fire off make_money():
            self.store.make_money()
            # if manager is unlocked, we should automate the money-making process:
            if self.store.manager_unlocked == True:
                self.start_timer()


# NOTE: we'll make an instance of the Store class for each of our stores!
class Store():
    # money, day and store_list are not associated with individual stores,
    # they are class variables, and hence are shared across all the Stores
    money = 25.00
    day = 1
    # set up an empty list:
    store_list = [] # to hold the stores

    # constructor for Store class: __init__(self) is the constructor
    # it'll get called automatically when the object is created (for the Store class)
    # in the init method, self refers to the newly created object
    def __init__(self, storename, storeprofit, storecost, timer, manager_cost, store_image, growth_factor):  # this is a parameterised constructor!
        # self -> refers to the instance oof the Store class:
        # We add 'self' before each of these variables so that they'll be
        # unique for each and every store we create:
        self.store_name = storename
        # a variable to hold the number of stores:
        # store_count should be zero, so as to not calculate wrong profit
        self.store_count = 0    # player starts out with 0 stores, has to buy first
        # each time its a new day, we wanna show the profit of the player's store(s):
        # the amount of money the player makes = store_count * store_profit
        # we are converting the params to float, because the data read from csv is passed as string, so we explicitly need to convert them
        self.store_profit = float(storeprofit)
        self.store_cost = float(storecost)
        self.timer = float(timer)  # our timer's gonna be, by default, for 5 seconds
        self.manager_unlocked = False   # we'll unlock managers to automate the money-making process
        self.manager_cost = float(manager_cost)    # the player will have to pay for unlocking the manager
        self.timer_object = StoreTimer(self)    # referencing through objects, this timer object will be called in the click_store, which will initiate the timer
        self.image = store_image
        self.growth_factor = float(growth_factor)

    # User-defined functions/ Class methods:
    # NOTE: in these class methods, self refers to the instance that called the method.
    # this method is only gonna be for the template of the class; not a unique method
    @classmethod
    def display_stores(cls): # cls -> class, not instance
        # displaying store name using label:
        store_label_col0 = tk.Label(root_window, text = "CLICK", font = "Arial 13 bold italic")
        store_label_col0.grid(row = 4, column = 0)  # label placement in a grid-like way
        store_label_col1 = tk.Label(root_window, text = "STORE NAME", font = "Arial 13 bold italic")
        store_label_col1.grid(row = 4, column = 1)  # label placement in a grid-like way
        # displaying store cost using label:
        progress_label = tk.Label(root_window, text = "PROGRESS", font = "Arial 13 bold italic")
        progress_label.grid(row = 4, column = 2)
        # displaying the progress bar label:
        store_label_col2 = tk.Label(root_window, text = "COST", font = "Arial 13 bold italic")
        store_label_col2.grid(row = 4, column = 3)
        # displaying store count using label:
        store_label_col3 = tk.Label(root_window, text = "COUNT", font = "Arial 13 bold italic")
        store_label_col3.grid(row = 4, column = 4)
        # displaying buy label:
        store_label_col4 = tk.Label(root_window, text = "BUY", font = "Arial 13 bold italic")
        store_label_col4.grid(row = 4, column = 5)
        # displaying unlock label:
        store_label_col5 = tk.Label(root_window, text = "UNLOCK MANAGER", font = "Arial 13 bold italic")
        store_label_col5.grid(row = 4, column = 6)

        i = 1   # to iterate inside store_list
        for store in cls.store_list:
            store.display_store_info(i) # display_store_info() is called here
            i += 1
        print(DIVIDER)

    def display_store_info(self, i):    # its called inside display_stores()
        # store button with a photo:
        self.photo_button = tk.Button(root_window, command = lambda : self.click_store())
        photo = PhotoImage(file='images/' + self.image)
        self.photo_button.config(image = photo, width = "40", height = "40")
        self.photo_button.image = photo
        self.photo_button.grid(row = 4 + i, column = 0, padx = 5)

        # store name label
        self.store_name_label = tk.Label(root_window, text = self.store_name)
        self.store_name_label.grid(row = 4 + i, column = 1, padx = padding)

        # progress bar!
        # we have to update the progress bar as the timer goes
        # the following code is to color our progress bar
        s = ttk.Style()
        s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground = 'red', background = 'red')
        # the 'mode = determinate' makes the progress bar animate; do not change it to 'inderminate'
        self.progress_bar = ttk.Progressbar(root_window, style = "red.Horizontal.TProgressbar", value = 0, maximum = 100, orient = tk.HORIZONTAL, length = 190, mode = 'determinate')
        self.progress_bar.grid(row = 4 + i, column = 2, padx = padding)

        # displaying store cost using label:
        self.store_cost_label = tk.Label(root_window, text = MONEY_FORMAT.format(self.store_cost))
        self.store_cost_label.grid(row = 4 + i, column = 3, padx = padding)
        # displaying store count using label:
        self.store_count_label = tk.Label(root_window, text = self.store_count)
        self.store_count_label.grid(row = 4 + i, column = 4, padx = padding)

        # the buy button:
        self.buy_button = tk.Button(root_window, text = "Buy %s" % MONEY_FORMAT.format(self.store_cost), width = 15, command = lambda : self.buy_store())
        self.buy_button.grid(row = 4 + i, column = 5, padx = padding)

        # buy manager button:
        self.manager_button = tk.Button(root_window, text = MONEY_FORMAT.format(self.manager_cost), width = 10, command = lambda : self.unlock_manager())
        self.manager_button.grid(row = 4 + i, column = 6, padx = padding)

    def buy_store(self):
        # using the growth factor:
        next_store_cost = self.store_cost * self.growth_factor * self.store_count + 1
        # check if the player has enough money to buy the store:
        if next_store_cost <= Store.money:
            # if the player has enough money, purchase a new store:
            self.store_count += 1
            Store.money -= next_store_cost
            # update the store count label, to show on the GUI:
            self.store_count_label.config(text = self.store_count)
            next_store_cost = self.store_cost * self.growth_factor * self.store_count
            self.buy_button.config(text = "Buy %s" % MONEY_FORMAT.format(next_store_cost))
            # update UI:
            game.update_UI()
        # else if the player has lesser money than store_cost, print message
        else:
            messagebox.showinfo("Not Enough Money!", "You don\'t have enough money to buy the store. Please try again after some time.")
            # return store_count_var, money_var -> not required since we are updating it right inside the method

    def unlock_manager(self):
        if self.manager_cost <= Store.money:
            self.manager_unlocked = True
            Store.money -= self.manager_cost
            self.manager_button.configure(state = "disabled")
            game.update_UI()
        else:
            messagebox.showinfo("Not Enough Money!", "You don\'t have enough money to unlock the manager. Please try again after some time.")

    def click_store(self):
        self.timer_object.start_timer()


    # click the button, and make the money
    def make_money(self):
        # each store will now have a different timer
        daily_profit = self.store_profit * self.store_count
        Store.money += daily_profit
        # update money label, after adding the profits to the player's total money:
        game.update_UI()

    @classmethod
    def advance_week(cls):
        for i in range(0, 7):
            cls.next_day()  # to advance a week, simply call next_day() 7 times!


# for a function returning multiple values
# you assign two variables while calling it to
# store the respective values
# store_count, money = buy_store(store_count, money)

# each game needs to have a game manager:
class GameManager():
    def __init__(self):
        # when we start up, first, create stores and display the game header:
        self.create_stores()
        self.display_game_header()
        # display stores list:
        Store.display_stores()

    def create_stores(self):
        # read data from file (data.csv):
        with open(data_file, newline = '') as file:
            reader = csv.reader(file)   # reader() returns a list
            for row in reader:
                Store.store_list.append(Store(*row))    # *row -> entire row

        # # create a new store and add the new store to our list:
        # Store.store_list.append(Store('Lemonade Stand', 4.5, 3, 3, 2))  # making our first manager 2 bucks, so that we can test it
        # Store.store_list.append(Store('Record Store', 5, 10, 10, 200))
        # Store.store_list.append(Store('Ice Cream Store', 60, 120, 6, 800))

    def display_game_header(self):
        # this function is used to display game stats
        # setting window attributes:
        root_window.title("EZ Business Tycoon")  # window title
        root_window.geometry(window_size)  # dimensions of the window
        # root_window.configure(background = 'white')

        # displaying money using labels:
        self.money_amount_label = tk.Label(root_window, text = MONEY_FORMAT.format(Store.money), font = "Arial 24 bold")
        self.money_amount_label.grid(row = 1, column = 0)

    # to update the GUI:
    def update_UI(self):
        # in update_UI(), we are updating the money label! -> it'll be called whenever amount of money changes
        self.money_amount_label.config(text = MONEY_FORMAT.format(Store.money))

#   NOTE: you don't wanna use the time.sleep() function for a timer, because
#         that will just lock up your gameplay, which is kinda against an
#         idle clicker.

print("Thank you for playing the EZ Business Tycoon Game!")

root_window = tk.Tk()


# start the game manager by creating its object (and initialising the constructor):
game = GameManager()

root_window.mainloop()



