#   Purpose: Creating a Business Tycoon game while learning the basics object-oriented programming in Python.
#   Note: The game will have a pretty basic GUI.
#   Day/Date: Saturday/6th October 2018
#   Author: Neeraj

MONEY_FORMAT = '${:0,.2f}'  # if we wanna change it, we can simply do it here, not inside the code!
DIVIDER = "==================================================="


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
    def __init__(self, storename, storeprofit, storecost):  # this is a parameterised constructor!
        # self -> refers to the instance oof the Store class:
        # We add 'self' before each of these variables so that they'll be
        # unique for each and every store we create:
        self.store_name = storename
        # a variable to hold the number of stores:
        # store_count should be zero, so as to not calculate wrong profit
        self.store_count = 0    # player starts out with 0 stores, has to buy first
        # each time its a new day, we wanna show the profit of the player's store(s):
        # the amount of money the player makes = store_count * store_profit
        self.store_profit = storeprofit
        self.store_cost = storecost

    # User-defined functions/ Class methods:
    # NOTE: in these class methods, self refers to the instance that called the method.
    # this method is only gonna be for the template of the class; not a unique method
    @classmethod
    def display_game_info(cls): # cls -> class, not instance
        # display game stats (money earned, day no):
        print(DIVIDER)
        print("Day #" + str(cls.day))
        print('Money = ' + MONEY_FORMAT.format(cls.money))
        print(DIVIDER)
        print('STORE LIST'.ljust(25) + 'STORE COST'.ljust(15) + 'STORE COUNT')  # ljust() -> left justify
        i = 1   # to iterate inside store_list
        for store in cls.store_list:
            store.display_store_info(i)
            i += 1
        print(DIVIDER)

    def display_store_info(self, i):
        # display store info like store count
        store_cost_str = MONEY_FORMAT.format(self.store_cost).rjust(12)
        print(str(i) + ")" + self.store_name.ljust(20) + store_cost_str.ljust(20) + str(self.store_count))

    @classmethod
    def buy_store(cls):
        try:
            which_store = int(input("Which Store Do You Wish To Buy? (1 - %s):" % len(Store.store_list)))
        except:
            print("Invalid input.\nBuy Aborted.")
            return

        if which_store >= 1 and which_store <= len(Store.store_list):
            store = Store.store_list[which_store - 1]   # which_store - 1 because list indices begin at 0
            # check if the player has enough money to buy the store:
            if store.store_cost <= Store.money:
                # if the player has enough money, purchase a new store:
                store.store_count += 1
                Store.money -= store.store_cost
            # else if the player has lesser money than store_cost, print message
            else:
                print("You don't have enough money.")
                # return store_count_var, money_var -> not required since we are updating it right inside the method
        else:
            print("Invalid input.")

    @classmethod    # since next_day() will update each store's profit, we need to make it a class method
    def next_day(cls):
        # increment the day
        cls.day += 1
        for store in cls.store_list:
            # if store hasn't been bought, its profit will be zero as its store_count var will be 0
            daily_profit = store.store_profit * store.store_count
            cls.money += daily_profit

    @classmethod
    def advance_week(cls):
        for i in range(0, 7):
            cls.next_day()  # to advance a week, simply call next_day() 7 times!


# for a function returning multiple values
# you assign two variables while calling it to
# store the respective values
# store_count, money = buy_store(store_count, money)
   
# create a new store and add the new store to our list:
Store.store_list.append(Store('Lemonade Stand', 1.5, 3))
Store.store_list.append(Store('Record Store', 5, 5))
Store.store_list.append(Store('Ice Cream Store', 60, 120))

# a simple game loop (quits when q/Q is pressed) -> for text-based interactions
while True:
    # call the class method:
    Store.display_game_info()

    print("Available options: (N)ext Day, (W)eek Advance, (B)uy Store, (Q)uit")
    result = input("Please Enter Your Selection: ")

    # if the player pressed 'B' or 'b'
    if result == 'B' or result == 'b':
        Store.buy_store()
    # if the player pressed 'N' or 'n'
    elif result == 'N' or result == 'n':
        Store.next_day()
    elif result.upper() == 'W':
        Store.advance_week()
    # if the player pressed 'Q' or 'q'
    elif result == 'Q' or result == 'q':
        break   # break out of the loop
    # if something else is pressed
    else:
        print("Bad input")


