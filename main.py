# Hearts with some AI LOL
# Donny Ebel
# MTH 205
# Fall 2021

# Credits:
# https://www.geeksforgeeks.org/print-colors-python-terminal/ for help with color printing!
# http://mark.random-article.com/hearts/terms.html for helpful terminology to think about the game differently!
# https://sites.ualberta.ca/~amw8/hearts.pdf for inspiration and thoughts on what can and can't be done!

# NOTE: Sort ordering for suits is as follows:  DIAMOND < CLUB < HEART < SPADE
#       Changing the macro will change the order everywhere, but may mess with AI a little...

# Updates:
# 12/12/21  -Cleaned up choose_card() by creating ai_choose_card() method. This moves the AI logic out of choose_card().
#           -Updated user_card in all 'choose' methods to be declared as a Card(). This prevents some confusing errors.
#           -Commented out a section of code that's supposed to remove the ♠Q if it's unsafe, but it was kinda buggy.
#           -Threw in some boolean if statements that print the AI's notes and/or WH and statuses that work most of the
#               time, which is good enough for me!
#           -Wrote the readme! Time for a break!
#
# 12/11/21  -Finished gather_game_data()
#           -Added variables to Game() to track if the user wants to see AI info or their working hands.
#
#           TODO:
#           -Add functionality to show AI info and working hands!
#           -Make clean up choose_card() by making more methods such as a method to eval statuses in WH!
#           -Sometimes if the AI is in make_a_decision() and has one out SPADE, but a low SPADE count, they'll play the
#               out and screw themselves if someone else plays a SPADE.
#
# 12/10/21  -Spent a lot of time fleshing out the AI decisions in choose_card(). Sometimes the AI knows that a high
#               card is safe when they shouldn't, but that's a consequence of gen_all_poss_tricks() playing ahead. See
#               next steps.
#           -The AI's use of make_a_decision() to choose a card in a hand of many suits and/or statuses is the fuzziest
#               part of the logic. When this function is called, the AI is either leading or void in the trick_suit, so
#               USUALLY the best play is to play the highest rank in the WH. Also, if there is a tie in rank, it will
#               probably choose the "highest" suit in order DIAMOND < CLUB < HEART < SPADE, but this is very rare.
#           -Created a number of 'choose'-type methods and other static helper methods to assist in making decisions.
#               I am somewhat ashamed of which_card_is_higher_rank(), but there isn't a way to compare naked ranks with
#               > or < that works correctly without making a Rank() class and overloading those magic methods, which
#               seems silly.
#           -Added self.game_over bool to Game(). Now play_the_game plays as many games as needed for someone to get to
#               100 points.
#           -Wrote a function to collect needed data from the user to play Hearts! Everything will be returned via tuple
#               and passed to Game() to build what it needs to play the game.
#
#           NEXT TIME:
#           -Finish gather_game_data().
#           -Add flags to Game() regarding whether or not the user wants to see AI notes or their WH or whatever and
#               make sure it works!
#           -Polish!
#
#           NEXT STEPS:
#           -After adding highest and lowest three cards of each suit to statuses (with appropriate updating), consider
#               removing tricks with data that occurs on a later player's turn from all_poss_tricks. Then the AI can
#               have a little more info to choose a card realistically, especially when leading where there is the least
#               amount of data.
#           -Use this engine to develop card weights for a stronger type of AI down the road.
#
#           TO DO:
#           -Make clean up choose_card() by making more methods such as a method to eval statuses in WH!
#           -Sometimes if the AI is in make_a_decision() and has one out SPADE, but a low SPADE count, they'll play the
#               out and screw themselves if someone else plays a SPADE.
#
# 12/09/21  -Moved human input processing into its own function get_human_input() so I can insert human input wherever I
#               find useful.
#           -Added the card played by the active player to the tuple storing poss trick info. Now it holds the card they
#               played, points in the trick, and who takes it.
#           -Fixed a bug in who_takes_the_trick() by changing the suit of the Card returned by the default
#               Card.__init__() to SUITS[0]. It was CLUB causing tricks of diamonds to not select the highest_card
#               properly.
#           -Began constructing an AI algorithm to be called from choose_card() by playing several games while looking
#               at all the stats.
#           -Added self.void_suits list to Player class. Also updated long suits to be 6 or more cards of a suit and
#               made that a list to match the others.
#           -Overhauled print_stats() to show useful info (like voids). Void suits may be important to AI! Same with
#               3 highest and lowest cards that are still unplayed (especially outs), but I'll probably add that later.
#           -Added a line in play_the_game() to only call gen_all_possible_tricks() if len(working_hand) > 1 so we don't
#               have to do all that extra work since choose_card() will always play the card if len(working_hand) == 1.
#           -Added statuses to Card objects. This lets AI assign a value to each card based on board state, etc. The
#               statuses are OUT, SAFE, and UNSAFE. Also made HIGH, but may not use it.
#           -Wrote eval_safety() to let AI assign statuses to cards in the working_hand. Refining.
#           -AI now chooses the best card if WH is all one suit. This takes care of many cases. The AI still has trouble
#               leading and what to play if void in the trick_suit. Once I write those cases, it should be able to
#               handle MOST situations...
#           -Wrote a number of helper methods to assist, and some more methods in Card for simple status manipulations.
#           -Formatting.
#           -Made a tiny algorithm that may be useful for teaching AI to lead and when void.
#
#           NEXT TIME:
#           -Teach AI how to lead and how to choose a card when void in the trick_suit. May just need to teach it how to
#               know when to choose a particular suit, and then a particular card status.
#           -Look at eval_safety():
#               -Do I believe that it needs to assign Card status differently if leading?
#               -Do I believe that it needs to assign Card status differently based on Game.suit_counts (dict)?
#
#           (Probably not enough time for anything else but also):
#           -Add tracking for three highest and three lowest cards in each suit.
#           Add records in Card class to track its status over the course of the game (very cool!).
#           Maybe add toppers and stoppers after implementing shooting the moon in the far future LOL
#
# 12/08/21  -Added a turn count parameter to gen_all_poss_tricks() to init hands correctly based on turn.
#           -Added a call to gen_all_poss_tricks() in play_the_game(). This also inits WHs correctly, so removed
#               the call to p.init_working_hand(). There is one small exception that may produce strange WH for non-lead
#               players if the WH aren't initialized again after a card is led; added a note in the func about that.
#               However, all players' WH are initialized before choosing a card, so no problems arise in the main loop.
#           -Rewrote count_all_points() to count shooting the moon correctly!
#           -Moved trick_suit and hearts_broken updates out of the main game loop and into update_game_records().
#           -Mucked around with some formatting.
#           -Rewrote who_takes_the_trick() because it was having issues finding the index in a list of Cards. It also
#               now requires the trick to evaluate to be passed in so it can be useful in more contexts.
#           -Added a line to update the working trick before attempting to gen_all_poss_tricks() in the main loop. Now
#               the tricks generated have earlier players' cards added correctly.
#           -Added functionality to gen_all_poss_tricks() that creates a list of tuples to store the value of the
#               tricks generated (i.e. points and who takes the trick).
#           -Created functions to print and clear all_poss_tricks.
#           -Even more formatting! I didn't end up using int_game_state_copy() that I made earlier... Might delete it!
#
#           NOW:
#           -Analyze books in all_poss_tricks for points and who takes it       DONE
#           -Use this data to think about how to lead
#
#           AI Thoughts:
#           Level 0 AI:     Never take/lead the queen of spades unless it's the only option.
#                           Avoid taking points.
#                           Tries to get rid of short suits.
#           Level 1 AI:     Randomly choose a card among the tricks that take no points. If all take points, choose a
#                           random card.
#           Level 2 AI:     Will play a high card if he gains no points.
#           Level 3 AI:     Plays high only if he has an out.
#           Level + AI:     Tries to shoot the moon! LOL
#
#           NEXT TIME:
#           Begin to implement AI       STARTED
#           Add tracking to Player for voids (no cards in a suit) to stats      DONE
#           Add tracking for the three highest cards and lowest cards in a suit. Low cards can be used as "outs".   SOON
#           Maybe add a "self.status" variable for each card to track their value over the course of the game.
#               Identify cards such as the highest and lowest cards ('out cards') in a suit that change as cards are
#               played, and over this many games it had this status this percent of the time... Data to weight cards!
#           Create a way to view card statuses once implemented.        DONE
#           Maybe add toppers and stoppers after implementing shooting the moon in the far future LOL
#           Tiny note: an out is only an out if it's not the last of its suit! *because it sees the future it knows this
#
# 12/07/21  -Created a recursive algorithm to populate a list of all possible tricks on a given turn. The proper amount
#               of tricks should be all players' hand counts multiplied together (i.e. 4*1*4*3 = 48 possible tricks).
#           -Fleshed out the recursive func some. Still gotta test!     I TESTED IT AND IT WORKS :D
#           -Increased recursion depth to 10000 so both gen_all_poss_tricks() and deepcopy are happy.
#           -LATER:
#           Flesh it out and test it!   DONE
#           Create a func to score each book for the player that originally called the recursive func
#           Update CPU_AI in choose_card to pick the best card
#           Much later, add tracking to value cards over many games
#           -TO DO:
#               Need to update scoreboard to score shooting the moon correctly!     DONE
#               Successfully move trick_suit and hearts_broken updates into update_game_records func.       DONE
#               After doing ^ above, update the recursive function to update and rewind game records.       NO, IT WORKS
#               Update print_all_poss_tricks to print points and the name of the player who will take it.   DONE
#               Another thing I could do is replace the two for loops in remove funcs with a while loop that only
#                   increments if something isn't removed, which would work, but would it really matter?    NAH
#
# 12/06/21  -Created init_game_state_copy for use in AI development. After doing some reading, developing an AI with
#               perfect board knowledge may be easier than an imperfect one, so making a copy of the board and playing
#               that turn through to find the best card to play each turn may be the right strategy!
#           -An approach of this manner uses brute force to find a value of a card after it's played. I wonder if it
#               could be used to collect data. Remember, the original idea was to play a data-based game LOL
#           -Plan A: build a recursive function that unrolls (?) the hand from an incremented player_list. Some sig
#               like Game.recursive_func_name(self, p, p_index, book, ...). Base case would be if it's the last player
#               in the list. Return the chosen card of p_index + 1. It may be a good idea to order the Player's
#               working_hands by size for a boundary.
#           -Plan B: create a method in Game() to build a list of all possible books for the hand, score them based on
#           who takes the trick, and return a list of cards to choose from (or just one card!)
#           -Plan C: Combine them! Maybe use the recursive method to populate the list of books (but could just use
#               nested loops, even though that isn't as cool as recursion). Recursion might not even work lol
#           -Also need to update scoreboard to score shooting the moon correctly!
#
# 12/05/21  -In choose_card, if there's only one legally playable card in working_hand, just return that card!
#           -Moved update_interface calls around in main loop to make output make more sense
#
# 12/04/21  -Perfected what I'd started yesterday: choose_card now accepts human input. Created a static method to
#               ensure good input; couldn't think of a reason to make it not static.
#           -Rewrote print_scoreboard to just print the dict; good enough!
#           -Reworked choose_card to make it more clear that it returns cards; only random ai wants an index
#           -Added a line to always print the current player's working hand during their turn when running a game
#           NEXT TIME:
#           -Convert the for loop at the beginning of play_the_game into a while that tracks player scores
#           -Change the scoreboard dict keys to accomplish the above entry
#           -Update scoreboard to score shooting the moon correctly
#           -Start coding some AI!! :) :) Use trees to look into the future to test playing different cards, then decide
#               what to play based on whether you want to take the trick or not, plus other settings! MiniMax?!     NOPE
#
# 12/03/21  -Changed ints in RANKS into strings, then updated the necessary magic methods and manually-crafted Cards
#               everywhere to accept this change.
#           -Got frustrated so I stopped LOL
#
# 12/02/21  -Rewrote who_takes_the_trick to work properly by removing cards from a working trick instead of whatever
#               else it was I was trying to do
#           -Created an AI stub class
#           -Added a list and a dict to Game class to track all cards and suits played
#           -Fixed a bug where play_the_game never broke hearts when it was supposed to
#           -Fixed an indexing bug in choose_card where the index would always be -1 and never be updated (why? idk)
#           -Renamed uses of 'Player' as an index variable to just p
#           -Reworked init_working_hand to account for the case where you lead, heart's aren't broken, and you happen
#               to have a hand full of hearts
#           -Added a counter for games played to track LOTS of games if needed
#           NEXT TIME:
#           -Add a way to play as a human (it might be helpful to only see the working hand when playing)
#           -Use update_interface() to call another function to scorekeep with an option to print the scores?
#           -Make another function to display the score at the end of the game
#
# 12/01/21  -Changed Card magic methods to reference SUITS macro; just changing macro order now changes order everywhere
#
# 11/30/21  -Haven't been keeping track, first started around 11/10/21. I did have a slightly broken play_the_game()
#               completed along with some rudimentary printing
#           -LOTS of debugging
#           -Cleaned up the interface printing, including printing the trick in a clockwise pattern.
#           -Paced the main loop, adding [ENTER] and printing the interface at important intervals
#           -Made use of \n
#           -Enabled printing player's books
#           -Fixed a bug in all 'remove' functions where it would only remove every other card that it was supposed to
#           -Removed function print_deck (why do you need it)
#           # Next time:
#           -need to fix who_takes_the_trick() to choose the correct card   DONE NOW
#           -maybe print the player's hands right next to the clockwise representation and mess with spacing? :)    NO
#           -add a list that tracks and counts played suits to calc odds for data and future ai     DONE NOW


from random import shuffle, randint
from copy import deepcopy
import sys

# Macros and colored print functions / Note: "black" is really light gray
SPADE = '\u2660'    # These codes enable the console to print suit symbols!
DIAMOND = '\u2666'
CLUB = '\u2663'
HEART = '\u2665'
SUITS = [DIAMOND, CLUB, HEART, SPADE]  # Changing this order changes the order everywhere! May mess with AI...
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']  # Ace high
HUMAN_AI = 'human'  # AI tags
RANDOM_AI = 'rand'
CPU_AI = 'cpu'
OUT = 'out'
SAFE = 'safe'
UNSAFE = 'unsafe'
HIGH = 'high'
limit = 10000     # Increased recursion limit; needed for deepcopy and gen_all_poss_tricks()
sys.setrecursionlimit(limit)
def prBlack(string): print("\033[2m{}\033[00m".format(string), end="")  # These functions enable printing in color
def prRed(string): print("\033[31m{}\033[00m".format(string), end="")
def prGreen(string): print("\033[32m{}\033[00m".format(string), end="")
def prBlue(string): print("\033[94m{}\033[00m".format(string), end="")
def prPurple(string): print("\033[95m{}\033[00m".format(string), end="")
def prCyan(string): print("\033[96m{}\033[00m".format(string), end="")


# Create game: Hearts
class Game:
    def __init__(self, name1, name2, name3, name4, ai1, ai2, ai3, ai4, ai_notes, ai_wh, num_humans, num_ai):
        self.deck = []
        self.player_list = [Player(name1, ai1), Player(name2, ai2), Player(name3, ai3), Player(name4, ai4)]
        self.north = self.player_list[0]    # used to cycle to North again; kinda silly but unsure of a better way
        self.trick = []  # this is the space where cards are played
        self.trick_suit = None  # tracks the required suit to play into the trick
        self.hearts_broken = False
        self.cards_played = []
        self.suit_count = dict.fromkeys(SUITS, 0)
        self.scoreboard = dict.fromkeys(self.player_list, 0)
        self.game_over = False
        self.ai_notes = ai_notes        # fixme add this functionality!
        self.print_wh = ai_wh           # fixme add this functionality!
        self.num_humans = num_humans
        self.num_ai = num_ai

        # Values for CPU_AI
        self.working_trick = []             # a working trick to assemble all_poss_tricks
        self.all_poss_tricks = []           # a gigantic list of all possible tricks for a given board state
        self.all_poss_tricks_scored = []    # a list of tuples: (points in the trick, who takes the trick)
        self.trick_count = 0                # a test value: may delete later

    # Primary Game methods
    def play_the_game(self):
        game_rounds = 0
        while not self.game_over:     # while no player >= 100 points
            game_rounds += 1
            self.start_round()      # creates and shuffles deck, deals, and cycles to correct player
            # self.pass()           # pass when implemented lol
            for turn in range(1, 14):
                p_index = 0     # tracks the index of the player whose turn it is
                for p in self.player_list:  # choose/play a card, then update trick_suit, hearts_broken, and interface
                    self.update_working_trick()         # populates working_trick
                    p.init_working_hand(turn, self.trick_suit, self.hearts_broken)
                    if len(p.working_hand) > 1:         # if > 1 card in WH, gens all_poss_tricks
                        self.gen_all_poss_tricks(turn, p, p_index, deepcopy(p_index))
                    self.update_interface(game_rounds, turn)            # update interface and print appropriate WH
                    self.print_appropriate_hands(p)
                    card = p.choose_card(turn, p_index, self.trick_suit, self.all_poss_tricks_scored, self.cards_played,
                                         self.ai_notes, self.print_wh)
                    self.trick.append(p.play_card(card))    # play the card; pop card into trick
                    self.update_game_records(card)          # updates trick_suit, hearts_broken, and various stats
                    p_index += 1
                # Determine who takes the trick and update board state
                self.update_interface(game_rounds, turn)
                winner = self.who_takes_the_trick(self.trick)     # give the trick to the 'winner'
                prPurple(winner)        # print who takes it and maybe wait for ENTER
                print(' takes the trick!')
                if self.num_humans:
                    input('[ENTER]')                # for human players; uncomment if needed
                self.take_trick(winner)         # side effect: trick is now empty
                self.cycle_to_player(winner)    # update turn order
                self.trick_suit = None          # reset trick suit
            # Round over; clean up
            print('\n=====GAME OVER=====\n')
            self.cycle_to_player(self.north)        # cycle to first player for printing scores
            self.print_all_books()
            self.count_all_points()
            self.print_scoreboard()
            input('[ENTER]')
            self.refresh_table()    # clear all hands, books, and stats; resets hearts_broken

    def print_appropriate_hands(self, p):
        # Prints appropriate hands during play!
        if p.ai == HUMAN_AI:
            p.print_hand(True)
        elif p.ai == CPU_AI or p.ai == RANDOM_AI:
            p.print_hand(True)
            if self.print_wh:
                p.print_working_hand()

    def gen_all_poss_tricks(self, turn, p, p_index, active_p_index):
        # Populates self.all_poss_tricks, a massive list of all tricks possible. Takes into account leading and
        # breaking hearts. It winds and unwinds through each players' working hand recursively to gen all poss combos.
        # p_index is used to track where we are in the recursive calls, while active_p_index isn't incremented with
        # p_index; instead, active_p_index lets us save the card played by the active player for that turn.
        # NOTE: If p is the lead player, only their WH is reliably init'd. Other players' WH will be init'd as if the
        #   trick_suit is the last suit in the lead's hand as a side effect. However, this doesn't matter in the main
        #   game loop since all players' WH are init'd again on subsequent calls to this func before choosing a card.
        p.init_working_hand(turn, self.trick_suit, self.hearts_broken)  # always init working hand
        new_trick_suit = False
        hearts_were_broken = False

        if p_index == 3:  # BASE CASE: for each card in WH, play, add trick to book, then pop, repeat w/ next card
            for card in p.working_hand:
                self.working_trick.append(card)  # add the appropriate card to the working trick
                self.trick_count += 1       # to test; might delete later
                if not self.hearts_broken and card.suit == HEART:  # if a heart is played (legally), update and note
                    self.hearts_broken = True
                    hearts_were_broken = True
                copy_of_working_trick = deepcopy(self.working_trick)    # Make a copy of working_trick, then add to
                self.all_poss_tricks.append(copy_of_working_trick)      # all_poss_tricks and store info as tuple
                self.all_poss_tricks_scored.append((copy_of_working_trick[active_p_index],
                                                    self.count_points_in_the(copy_of_working_trick),
                                                    self.who_takes_the_trick(copy_of_working_trick)))
                self.working_trick.pop()    # pop to play the next card in WH or prepare to return to prev player
                if hearts_were_broken:  # reset hearts_broken if needed
                    self.hearts_broken = False
            return

        else:  # Add a card to the trick, update trick_suit and hearts_broken, then call func with the next player
            for card in p.working_hand:
                self.working_trick.append(card)  # add the appropriate card to the working trick
                if not self.trick_suit:  # if not trick_suit, update note that it was updated
                    self.trick_suit = card.suit
                    new_trick_suit = True
                if not self.hearts_broken and card.suit == HEART:  # if a heart is played (legally), update and note
                    self.hearts_broken = True
                    hearts_were_broken = True
                self.gen_all_poss_tricks(turn, self.player_list[p_index + 1], p_index + 1, active_p_index)

                # Once we've returned, remove the played card, then reset trick_suit/hearts_broken if they changed
                self.working_trick.pop()
                if new_trick_suit:
                    self.trick_suit = None
                if hearts_were_broken:
                    self.hearts_broken = False
            return

    def update_interface(self, game_num, turn_num):
        # Prints the interface, woo!
        print('\n\n')
        # print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')  # for screen-scrolling; comment out if needed
        prCyan('Game ')
        prCyan(game_num)
        print(' | ', end='')
        prPurple('Turn ')
        prPurple(turn_num)
        print(' ', self.player_list)
        print('Hearts Broken:', self.hearts_broken)
        self.print_trick_suit()
        self.print_trick()
        # self.print_all_hands()                # for testing
        # self.print_cards_played()             # for testing
        # self.print_suit_count()               # for testing
        # self.print_all_working_hands()        # for testing
        print('')

    def update_game_records(self, card):
        # When a card is played, adjusts trick_suit, hearts_broken, clears all_poss_tricks/all_poss_tricks_scored and
        # adds parameter card to cards_played list and suit_count dict.
        if not self.trick_suit:                             # if not trick_suit, update
            self.trick_suit = card.suit
        if not self.hearts_broken and card.suit == HEART:   # if a heart is played (legally), update
            self.hearts_broken = True
        self.clear_all_poss_tricks()
        self.cards_played.append(card)                      # add card to list of played cards and suit_count dict
        self.suit_count.update({card.suit: self.suit_count.get(card.suit) + 1})
        self.trick_count = 0        # used to test; may delete later

    # Secondary Game methods; i.e. helper methods
    def start_round(self):
        # Creates a deck, shuffles, and deals, then cycles player list to whoever has the 2 of clubs
        self.create_deck()
        self.shuffle_deck()
        self.deal()  # also sorts hands and accumulates data
        self.cycle_to_player(self.who_is_holding_the(Card(CLUB, '2', 0)))

    def create_deck(self):
        # Adds all cards to the deck with appropriate point values; Card(suit, rank, points)
        for suit in SUITS:
            for rank in RANKS:
                points = 0
                if suit == HEART:
                    points = 1
                elif suit == SPADE and rank == 'Q':
                    points = 13
                self.deck.append(Card(suit, rank, points))

    def shuffle_deck(self):
        # Simply shuffles the deck
        shuffle(self.deck)

    def deal(self):
        # Deals 13 cards to each player, then has players sort their hands
        if not self.deck:
            print("error: can't deal an empty deck!")
            return
        for i in range(0, 13):
            for j in range(0, 4):
                self.player_list[j].hand.append(self.deck.pop())
        self.sort_all_hands()

    def cycle_player(self):
        # Used to manage turn order. Pops the player in index 0 and appends them to the end of the player_list
        self.player_list.append(self.player_list.pop(0))

    def cycle_to_player(self, new_lead_player):
        # Used to manage turn order. Calls cycle_player repeatedly to move the new_lead_player to the lead position [0]
        while self.player_list[0] != new_lead_player:
            self.cycle_player()

    def who_is_holding_the(self, card):
        # Returns the player holding the specified card
        for p in self.player_list:
            if p.hand.count(card):
                return p

    def who_takes_the_trick(self, trick):
        # Returns the Player who played the highest ranked card of the trick_suit in the parameter trick. Assumes cards
        # are added to the trick in the same order as the player_list (dependent on correct cycling) AND that
        # trick_suit is set properly.
        i = 0
        highest_card = Card()
        highest_card_index = i

        for card in trick:
            if card.suit == self.trick_suit:
                if card > highest_card:
                    highest_card = card
                    highest_card_index = i
            i += 1

        return self.player_list[highest_card_index]

    def take_trick(self, p):
        # Moves the trick to that player's book and clears the trick
        p.book.append(deepcopy(self.trick))  # uses deepcopy to avoid reference errors
        self.clear_trick()

    def update_working_trick(self):
        # Updates the working_trick
        self.working_trick = deepcopy(self.trick)

    def refresh_table(self):
        # Resets hearts_broken and clears each Player's current hand, working_hand, book, and various stats
        self.hearts_broken = False
        self.clear_cards_played()   # clears both self.cards_played and self.suit_count
        for p in self.player_list:
            p.clear_all()           # Clears each players' hand, book, working_hand, and various stats
        self.is_it_game_over()

    def is_it_game_over(self):
        for p in self.player_list:
            if self.scoreboard.get(p) >= 100:
                self.game_over = True
                break

    # Data methods: sort, count, print, and clear methods
    @staticmethod
    def count_points_in_the(trick):
        # Returns the number of points in the provided trick. Used in gen_all_poss_tricks().
        points = 0
        for card in trick:
            points += card.points
        return points

    def sort_all_hands(self):
        # Sorts each player's hand
        for p in self.player_list:
            p.sort_hand()

    def count_all_points(self):
        # Counts points in all player's books and adds them to the scoreboard dict.
        # Use of i is a little clumsy, but it works for now
        p_point_list = [0, 0, 0, 0]
        i = 0

        for p in self.player_list:      # count points and update p_point_list
            for trick in p.book:
                for card in trick:
                    p_point_list[i] += card.points
            i += 1

        if p_point_list.count(26):      # if someone shot the moon, update p_point_list accordingly
            for i in range(0, 4):
                if p_point_list[i] == 0:
                    p_point_list[i] = 26
                else:
                    p_point_list[i] = 0

        i = 0
        for p in self.player_list:
            self.scoreboard.update({p: self.scoreboard.get(p) + p_point_list[i]})
            i += 1

    def print_trick_suit(self):
        print('Trick Suit:', end=' ')
        if self.trick_suit == HEART or self.trick_suit == DIAMOND:
            prRed(self.trick_suit)
        else:
            prBlack(self.trick_suit)
        print('')

    def print_trick(self):
        # Prints the trick in a clockwise table fashion
        # This block prints the upper trick
        print('     [', end='')
        if len(self.trick) >= 1:
            if self.trick[0].suit == DIAMOND or self.trick[0].suit == HEART:
                prRed(self.trick[0])
            else:
                prBlack(self.trick[0])
        else:
            print('  ', end='')
        print(']')

        # Print fourth and second tricks
        print('[', end='')
        if len(self.trick) >= 4:
            if self.trick[3].suit == DIAMOND or self.trick[3].suit == HEART:
                prRed(self.trick[3])
            else:
                prBlack(self.trick[3])
        else:
            print('  ', end='')
        print(']      [', end='')
        if len(self.trick) >= 2:
            if self.trick[1].suit == DIAMOND or self.trick[1].suit == HEART:
                prRed(self.trick[1])
            else:
                prBlack(self.trick[1])
        else:
            print('  ', end='')
        print(']')

        # Print third trick
        print('     [', end='')
        if len(self.trick) >= 3:
            if self.trick[2].suit == DIAMOND or self.trick[2].suit == HEART:
                prRed(self.trick[2])
            else:
                prBlack(self.trick[2])
        else:
            print('  ', end='')
        print(']')

    def print_working_trick(self):
        # Prints the working trick in a clockwise table fashion
        # The style doesn't really matter; this was only used for testing the recursive func
        # This block prints the upper trick
        print('     [', end='')
        if len(self.working_trick) >= 1:
            if self.working_trick[0].suit == DIAMOND or self.working_trick[0].suit == HEART:
                prRed(self.working_trick[0])
            else:
                prBlack(self.working_trick[0])
        else:
            print('  ', end='')
        print(']')

        # Print fourth and second tricks
        print('[', end='')
        if len(self.working_trick) >= 4:
            if self.working_trick[3].suit == DIAMOND or self.working_trick[3].suit == HEART:
                prRed(self.working_trick[3])
            else:
                prBlack(self.working_trick[3])
        else:
            print('  ', end='')
        print(']      [', end='')
        if len(self.working_trick) >= 2:
            if self.working_trick[1].suit == DIAMOND or self.working_trick[1].suit == HEART:
                prRed(self.working_trick[1])
            else:
                prBlack(self.working_trick[1])
        else:
            print('  ', end='')
        print(']')

        # Print third trick
        print('     [', end='')
        if len(self.working_trick) >= 3:
            if self.working_trick[2].suit == DIAMOND or self.working_trick[2].suit == HEART:
                prRed(self.working_trick[2])
            else:
                prBlack(self.working_trick[2])
        else:
            print('  ', end='')
        print(']\n')

    def print_all_poss_tricks(self):
        # Prints the book of all_poss_tricks.
        i = 0
        for book in self.all_poss_tricks:
            print(' [ ', end='')
            for card in book:
                if card.suit == DIAMOND or card.suit == HEART:
                    prRed(card)
                    print('', end=' ')
                else:
                    prBlack(card)
                    print('', end=' ')
            print('] ', end='\t')
            # (self.all_poss_tricks_scored[i])
            for item in self.all_poss_tricks_scored[i]:
                if type(item) == Card:
                    if item.suit == DIAMOND or item.suit == HEART:
                        prRed(item)
                    else:
                        prBlack(item)
                    print('', end='\t')
                else:
                    print(item, end='\t')
            print('')
            i += 1
        print('len: ', len(self.all_poss_tricks))

    def print_all_hands(self):
        # Prints each player's hand, stats, and books in list order
        for p in self.player_list:
            p.print_hand(True)  # True here prints the players' names
            # p.print_book()

    def print_all_working_hands(self):
        for p in self.player_list:
            p.print_working_hand()
            print('')

    def print_all_books(self):
        for p in self.player_list:
            prBlue(p.name)
            if p.book:
                p.print_book()
            else:
                print(' [ ]')

    def print_cards_played(self):
        # Sorts and prints the list of played cards in each round
        self.cards_played.sort()
        print('Cards Played: ', end='')
        for card in self.cards_played:
            if card.suit == DIAMOND or card.suit == HEART:
                prRed(card)
            else:
                prBlack(card)
            print('', end=' ')
        print('')

    def print_suit_count(self):
        # Displays tallies of played suits this round
        print('Suits Played:', end=' ')
        for suit in SUITS:
            if suit == DIAMOND or suit == HEART:
                prRed(suit)
            else:
                prBlack(suit)
            print(self.suit_count.get(suit), end=' ')
        print('')

    def print_all_stats(self):
        # Prints player name and stats for their current hand
        for p in self.player_list:
            prBlue(p.name)
            p.print_stats()

    def print_scoreboard(self):
        print(self.scoreboard)

    def clear_trick(self):
        # Simply clears the trick
        self.trick.clear()

    def clear_all_poss_tricks(self):
        # Clears self.all_poss_tricks and self.all_poss_tricks_scored
        self.all_poss_tricks.clear()
        self.all_poss_tricks_scored.clear()

    def clear_all_hands(self):
        # Clears all hands and stats
        for p in self.player_list:
            p.clear_hand()

    def clear_cards_played(self):
        # Clears self.cards_played and self.suit_count
        self.cards_played.clear()
        self.clear_suit_counts()

    def clear_suit_counts(self):
        # Clears AI suit counts
        for suit in SUITS:
            self.suit_count.update({suit: 0})


# Create players
class Player:
    def __init__(self, p_name, p_ai):
        self.name = p_name
        self.ai = p_ai    # atm just a string naming the ai
        self.hand = []
        self.working_hand = []
        self.book = []  # list of tricks (each of which is a list)

        # Hand stats
        self.num_cards_in_hand = len(self.hand)
        self.points_in_hand = 0
        self.suit_count = dict.fromkeys(SUITS, 0)
        self.long_suits = []   # long suit means 6 or more of a suit in hand
        self.short_suits = []   # short suit means 2 or fewer of a suit in hand
        self.void_suits = []  # void suit is having 0 or more of a suit in hand

    def __str__(self):
        return "{}".format(self.name)

    def __repr__(self):
        return self.name

    # Primary Player methods
    def choose_card(self, turn, p_index, trick_suit, scored_tricks, cards_played, ai_notes, print_wh):
        # Returns the chosen card based on Player AI.
        user_card = Card()

        # For all AI, if you can only play one card, just play it!
        if len(self.working_hand) == 1 and self.ai != HUMAN_AI:
            if ai_notes:
                prPurple('Only one card in WH')     # fixme for testing
                print('')
            user_card = self.working_hand[0]

        # RANDOM_AI will choose a random index from the working hand
        elif self.ai == RANDOM_AI:
            user_card = self.working_hand[randint(0, len(self.working_hand) - 1)]

        # HUMAN_AI allows the user to choose a card
        elif self.ai == HUMAN_AI:
            user_card = self.get_human_input()

        # CPU_AI attempts to choose a card!
        elif self.ai == CPU_AI:
            user_card = self.ai_choose_card(turn, p_index, trick_suit, scored_tricks, cards_played, ai_notes, print_wh)

        return user_card

    def ai_choose_card(self, turn, p_index, trick_suit, scored_tricks, cards_played, ai_notes, print_wh):
        # Returns the card chosen by the AI!
        user_card = Card()

        # Evaluate the data; could make a func out of this with self status counts for WH; maybe later
        self.eval_safety(self.working_hand, scored_tricks)
        if print_wh:
            self.print_status_of_cards_in(self.working_hand)  # fixme for testing; b: OUT; g: SAFE; r: UNSAFE
        status_t = self.count_status_of_cards_in(self.working_hand)  # returns tuple of ints: (OUT, SAFE, UNSAFE)
        out = status_t[0]  # temp vars for readability
        safe = status_t[1]
        unsafe = status_t[2]
        # Remove unsafe cards if there are other options.   011, 110, 111, 101    <-- binary rep of logic
        if (not out and safe and unsafe) or \
                (out and safe and not unsafe) or \
                (out and safe and unsafe) or \
                (out and not safe and unsafe):
            self.remove_status(UNSAFE)
        # If I have an unsafe ♠Q and at least one other card in my hand, think about removing ♠Q, ♠K, or ♠A!
        # if self.do_i_have_the(Card(SPADE, 'Q', 13, UNSAFE)) and len(self.working_hand) > 1:
        #    self.remove_card(Card(SPADE, 'Q', 13))
        #    if self.do_i_have_the(Card(SPADE, 'K', 0, UNSAFE)) and len(self.working_hand) > 1:
        #        self.remove_card(Card(SPADE, 'K', 0, UNSAFE))
        #        if self.do_i_have_the(Card(SPADE, 'A', 0, UNSAFE)) and len(self.working_hand) > 1:
        #            self.remove_card(Card(SPADE, 'A', 0))
        #    prPurple('Removed an unsafe ♠Q, whew!')  # fixme for testing; there's a bug in here!
            print('')

        # If WH is all one suit, play the highest OUT or SAFE card.
        if self.is_working_hand_all_one_suit():
            if ai_notes:
                prPurple("All out/safe cards are of one suit")  # fixme for testing
                print('')
            if turn == 1 or out >= 2:
                user_card = self.choose_highest_safe_or_out()
                return user_card
            elif out:
                user_card = self.choose_highest_out()
                return user_card
            else:
                user_card = self.choose_highest_card_of_suit(self.working_hand, self.working_hand[0].suit)
                return user_card

        # If it's not a simple decision, then check if we lead.
        elif p_index == 0:
            if ai_notes:
                prPurple("Leading")  # fixme for testing
                print('')

            # Attempt a complex decision!
            user_card = self.make_a_decision(out)
            return user_card

        # If we aren't leading, then we're void in the trick_suit.
        elif self.suit_count.get(trick_suit) == 0:
            if ai_notes:
                if ai_notes:
                    prPurple('Void in trick suit')  # fixme for testing
                    print('')
            # Try to play a high SPADE
            if Card(SPADE, 'Q', 13) not in cards_played:
                if self.do_i_have_the(Card(SPADE, 'Q', 13)):
                    user_card = Card(SPADE, 'Q', 13)
                    return user_card
                elif self.do_i_have_the(Card(SPADE, 'A', 0)):
                    user_card = Card(SPADE, 'A', 0)
                    return user_card
                elif self.do_i_have_the(Card(SPADE, 'K', 0)):
                    user_card = Card(SPADE, 'K', 0)
                    return user_card
                else:
                    prPurple('Unable to play high ♠')  # fixme for testing
                    print('')
            # Can't play a high ♠, so get suit counts to try to play out a short suit or a HEART
            i = 0
            suit_count_list = [0, 0, 0, 0]
            for suit in SUITS:  # get suit counts
                suit_count_list[i] = self.suit_count.get(suit)
                i += 1
            # Try to play out a short suit
            if suit_count_list.count(1):  # if there's only one suit with one playable card, play it!
                suit_index = suit_count_list.index(1)
                suit_to_play = SUITS[suit_index]
                if ai_notes:
                    print('suit_to_play:', suit_to_play)
                self.remove_other_suits_except(suit_to_play)
                user_card = self.working_hand[0]
                return user_card
            else:
                if ai_notes:
                    prPurple('Unable to void a short suit of 1')  # fixme for testing
                    print('')
            # Try to play a HEART
            if suit_count_list[2]:      # fixme something wrong here and line 842??
                self.remove_other_suits_except(HEART)
                if len(self.working_hand) == 1:
                    user_card = self.working_hand[0]
                    return user_card
                else:
                    user_card = self.choose_highest()
                    return user_card
            else:
                if ai_notes:
                    prPurple('Unable to play a heart')  # fixme for testing
                    print('')
            # Void in trick_suit; can't play a high spade, short suit, or heart, so attempt a complex decision!
            user_card = self.make_a_decision(out)
            return user_card

        # To catch fallthrough
        else:
            prPurple('The AI is confused; please help:')
            print('')
            user_card = self.get_human_input()

            return user_card

    def init_working_hand(self, turn, trick_suit, hearts_broken):
        # Adjusts working_hand to hold only legally playable cards
        self.gen_stats()
        self.working_hand = deepcopy(self.hand)

        # 1st turn only
        if turn == 1:
            if not trick_suit:  # If you lead, remove all cards from working_hand and return, you're done!
                self.remove_all_but_card(Card(CLUB, '2', 0))
                return
            else:               # If you don't lead, you can't play point cards turn 1, so remove them
                self.remove_points()
        # All other turns:
        # If you're leading && HEARTs aren't broken && you don't have a hand of just HEARTs: remove HEARTs
        if not trick_suit and not hearts_broken and (self.suit_count.get(HEART) < len(self.hand)):
            self.remove_suit(HEART)
        # Otherwise, if you have the trick_suit, remove all other suits
        elif trick_suit and self.suit_count.get(trick_suit) > 0:
            self.remove_other_suits_except(trick_suit)

    def eval_safety(self, the_hand, scored_tricks):
        # For each card in the WH, assign a status based on scored_tricks. scored_tricks is a list of tuples: the 0
        # index of the item is a Card, the 1 index is the points in the trick, and the 2 index is the Player who will
        # take the trick.

        for card in the_hand:
            point_count = 0                         # reset point_count
            players_that_take_a_trick = set()       # make/clear the set

            # Analyze all tuples for that card
            for tup in scored_tricks:                         # for each tuple in the list: (card, points, 'winner')
                if tup[0] == card:                            # if we're looking at the right card:
                    if tup[2] == self:
                        point_count += tup[1]                 # care about points only if you take it
                    players_that_take_a_trick.add(tup[2])     # add the player who takes the trick to the set
            if self not in players_that_take_a_trick:
                card.status = OUT       # A card is an 'out' if never results in taking a trick
            elif point_count == 0:
                card.status = SAFE      # A card is 'safe' if it could take a 0-point trick
            else:
                card.status = UNSAFE    # A card is 'unsafe' if it could take a point trick

    def make_a_decision(self, num_outs):
        # If there are enough outs, play either safe or the out!
        prPurple('In make_a_decision()')        # fixme for testing
        print('')

        # If I have more than 2 outs, play highest safe or out. If just one out, play it!
        if num_outs > 0:
            if num_outs == 1:

                user_card = self.choose_highest_out()
            else:
                user_card = self.choose_highest_safe_or_out()

        # If hand is all one status, choose between suit and rank
        elif self.is_working_hand_all_one_status():
            prPurple('All one status')      # fixme for testing
            print('')
            # self.print_working_hand()
            user_card = self.choose_highest()

        # To catch fallthrough; shouldn't ever be here as all cases should be accounted for.
        else:
            prPurple('The AI is confused; please help:')
            print('')
            user_card = self.get_human_input()

        return user_card

    # Secondary Player methods: i.e. helper methods
    @staticmethod
    def eval_str_input(the_str):
        # Returns True if the_str can be manipulated to "SR" format; a str of suit followed by rank. False otherwise.
        # Side effects: changes the_str into the correct format
        if len(the_str) != 2 or the_str.isnumeric():  # return false if not exactly 2 characters or both are nums
            return False
        rank = the_str[0]
        suit = the_str[1]
        if the_str[1] in ['D', 'C', 'H', 'S']:  # If the suit was provided 2nd, swap the chars
            tmp = rank
            rank = suit
            suit = tmp
        if rank not in ['D', 'C', 'H', 'S'] or suit not in RANKS:  # If suit or rank aren't valid
            return False
        return True

    @staticmethod
    def which_card_is_higher_rank(card1, card2):
        # Returns the highest ranked Card, ignoring suits. Currently, there is no way to compare just the naked rank
        # with < or > without making a Rank() class.

        if not card2:
            return card1

        rank1 = card1.rank
        rank2 = card2.rank

        if rank1 == 'A':
            result = card1
        elif rank1 == 'K':
            if rank2 == 'A':
                result = card2
            else:
                result = card1
        elif rank1 == 'Q':
            if rank2 == 'K' or rank2 == 'A':
                result = card2
            else:
                result = card1
        elif rank1 == 'J':
            if rank2 == 'Q' or rank2 == 'K' or rank2 == 'A':
                result = card2
            else:
                result = card1
        elif rank1 == 'T':
            if rank2 == 'J' or rank2 == 'Q' or rank2 == 'K' or rank2 == 'A':
                result = card2
            else:
                result = card1
        elif rank2 == 'T' or rank2 == 'J' or rank2 == 'Q' or rank2 == 'K' or rank2 == 'A':
            result = card2
        elif int(rank1) > int(rank2):
            result = card1
        else:
            result = card2

        return result

    @staticmethod
    def choose_highest_card_of_suit(the_hand, the_suit):
        # Returns the highest card in the provided hand.
        # NOTE: For use only in hands of a single suit; otherwise comparison doesn't work properly.
        i = 0
        highest_card = Card()
        highest_card_index = i

        for card in the_hand:
            if card.suit == the_suit and card > highest_card:
                highest_card.rank = card.rank
                highest_card_index = i
            i += 1

        return the_hand[highest_card_index]

    @staticmethod
    def print_status_of_cards_in(the_hand):
        prGreen('\tHand Status:')
        print('', end='\t')
        for card in the_hand:
            card.print_status()
        print('')

    @staticmethod
    def count_status_of_cards_in(the_hand):
        # Returns the tallies of out, safe, and unsafe statuses in a tuple.
        num_out = 0
        num_safe = 0
        num_unsafe = 0

        for card in the_hand:
            if card.status == OUT:
                num_out += 1
            elif card.status == SAFE:
                num_safe += 1
            elif card.status == UNSAFE:
                num_unsafe += 1
        return num_out, num_safe, num_unsafe

    def choose_highest(self):
        # Returns the card with the highest rank regardless of SUIT. Higher indices in the WH may overwrite a card of
        # the same rank... :(
        highest_card = Card()

        for card in self.working_hand:
            if self.which_card_is_higher_rank(card, highest_card):
                highest_card = card

        return highest_card

    def choose_highest_out(self):
        # Returns the card with the highest rank with 'OUT' status.
        highest_card = Card()

        for card in self.working_hand:
            if card.status == OUT and self.which_card_is_higher_rank(card, highest_card):
                highest_card = card

        return highest_card

    def choose_highest_safe_or_out(self):
        highest_card = Card()

        for card in self.working_hand:
            if card.status == SAFE or card.status == OUT:
                highest_card = self.which_card_is_higher_rank(card, highest_card)

        return highest_card

    def get_human_input(self):
        # Handles taking and processing human input. Returns a card.
        user_card = Card()
        s = ''
        r = ''
        input_invalid = True
        card_not_in_hand = True

        while input_invalid or card_not_in_hand:
            prBlue(self.name)  # Print name and ask for input
            user_input = input(', enter your card: ')
            user_input = user_input.upper()

            # Ensure good input
            input_invalid = not self.eval_str_input(user_input)
            if input_invalid:
                continue  # if input is bad, start while loop over

            # Pull SUIT/RANK out of string and make requested card
            if user_input[0] in ['D', 'C', 'H', 'S']:
                s = user_input[0]
                r = user_input[1]
            elif user_input[1] in ['D', 'C', 'H', 'S']:  # If the suit was provided 2nd, swap the chars
                s = user_input[1]
                r = user_input[0]
            p = 0

            if s == 'D':
                s = DIAMOND
            elif s == 'C':
                s = CLUB
            elif s == 'H':
                s = HEART
                p = 1
            else:
                s = SPADE
                if r == 'Q':
                    p = 13
            user_card = Card(s, r, p)

            # Check to see if it's in working_hand
            if self.working_hand.count(user_card):
                card_not_in_hand = False

        return user_card

    def do_i_have_the(self, card):
        # Returns True if parameter card is in the WH; False otherwise.
        for c in self.working_hand:
            if c == card:
                return True
        return False

    def is_working_hand_all_one_suit(self):
        # Returns True if cards in the WH are all one suit; False otherwise.
        result = True
        test_suit = self.working_hand[0].suit

        for card in self.working_hand:
            if card.suit != test_suit:
                result = False
                break

        return result

    def is_working_hand_all_one_status(self):
        # Returns True if the cards in the WH are all one status; False otherwise.
        result = True
        test_status = self.working_hand[0].status

        for card in self.working_hand:
            if card.status != test_status:
                result = False
                break

        return result

    def remove_points(self):
        # Removes all point cards from the working_hand; tested and works
        cards_to_remove = []
        for card in self.working_hand:
            if card.points > 0:
                cards_to_remove.append(card)
        for card in cards_to_remove:
            self.working_hand.remove(card)

    def remove_card(self, card_to_remove):
        for card in self.working_hand:
            if card == card_to_remove:
                self.working_hand.remove(card)
                break

    def remove_suit(self, suit):
        # Removes all cards of the parameter suit from the working_hand; tested and works
        cards_to_remove = []
        for card in self.working_hand:
            if card.suit == suit:
                cards_to_remove.append(card)
        for card in cards_to_remove:
            self.working_hand.remove(card)

    def remove_other_suits_except(self, trick_suit):
        # Removes all suits other than the lead_suit from the working_hand; tested and works
        cards_to_remove = []
        for card in self.working_hand:
            if card.suit != trick_suit:
                cards_to_remove.append(card)
        for card in cards_to_remove:
            self.working_hand.remove(card)

    def remove_all_but_card(self, card_to_keep):
        # Removes all cards but the parameter card_to_keep from the working_hand; tested and works
        cards_to_remove = []
        for card in self.working_hand:
            if card != card_to_keep:
                cards_to_remove.append(card)
        for card in cards_to_remove:
            self.working_hand.remove(card)

    def remove_status(self, status):
        # Removes cards of the provided status from the WH.
        cards_to_remove = []
        for card in self.working_hand:
            if card.status == status:
                cards_to_remove.append(card)
        for card in cards_to_remove:
            self.working_hand.remove(card)

    def play_card(self, card):
        # Pops the card from the hand; doesn't check to see if card is in hand atm
        # print('Chosen Card:', end=' ')       # for testing
        # if card.suit == DIAMOND or card.suit == HEART:
        #     prRed(card)
        # else:
        #     prBlack(card)
        # print('')
        # input('[ENTER]')
        return self.hand.pop(self.hand.index(card))

# Data methods: sort, count, print, and clear methods
    def gen_stats(self):
        # Counts number of cards in hand, points, suits, long suit, and short suits in hand
        self.count_cards_in_hand()
        self.count_suits_in_hand()
        self.count_points_in_hand()

    def sort_hand(self):
        # Sorts hand and calls gen_stats
        self.hand.sort()
        self.gen_stats()

    def count_suits_in_hand(self):
        # Clear both suit_count list and dict and recounts hand
        self.clear_suit_counts()
        for card in self.hand:
            self.suit_count.update({card.suit: self.suit_count.get(card.suit) + 1})
        for suit in SUITS:
            if self.suit_count.get(suit) == 0:
                self.void_suits.append(suit)
            elif self.suit_count.get(suit) <= 2:
                self.short_suits.append(suit)
            elif self.suit_count.get(suit) >= 6:
                self.long_suits.append(suit)

    def count_cards_in_hand(self):
        # Counts number of cards in hand
        self.num_cards_in_hand = len(self.hand)

    def count_points_in_hand(self):
        # Counts points in hand
        for card in self.hand:
            self.points_in_hand += card.points

    def print_hand(self, print_name):
        # Prints the player's name if print_name followed by their current hand
        if print_name:
            prBlue(self.name)
            print('', end='\t')
        if self.hand:
            for card in self.hand:
                if card.suit == HEART or card.suit == DIAMOND:
                    prRed(card)
                elif card.suit == SPADE or card.suit == CLUB:
                    prBlack(card)
                print('', end=' ')
        else:
            print('[ ]', end='')
        print('')

    def print_working_hand(self):
        # Prints the player's name and working hand
        # prBlue(self.name)
        prGreen("\tLegal Plays:")
        print('', end='\t')
        for card in self.working_hand:
            if card.suit == HEART or card.suit == DIAMOND:
                prRed(card)
            elif card.suit == SPADE or card.suit == CLUB:
                prBlack(card)
            print('', end=' ')
        print('')

    def print_scored_tricks(self, scored_tricks):
        # Prints all the tuples in scored_tricks (which is Game.poss_all_tricks_scored). If the active player takes the
        # trick, prints their name in red.
        for item in scored_tricks:
            for thing in item:
                if type(thing) == Card:
                    if thing.suit == DIAMOND or thing.suit == HEART:
                        prRed(thing)
                        print('', end=' ')
                    else:
                        prBlack(thing)
                        print('', end=' ')
                elif type(thing) == int:
                    print(thing, end=' ')
                elif thing == self:
                    prRed(thing)
                else:
                    prBlack(thing)
            print('')

    def print_book(self):
        for trick in self.book:
            print(' [ ', end='')
            for card in trick:
                if card.suit == HEART or card.suit == DIAMOND:
                    prRed(card)
                elif card.suit == SPADE or card.suit == CLUB:
                    prBlack(card)
                print(' ', end='')
            print(']', end='')
        if self.book:
            print('')

    def print_stats(self):
        # Prints suit counts, long suits and short suits
        # Kinda ugly, but unsure of how to organize better or even if it should be split into helper functions
        print('', end='\t\t')

        # Print long suits or None
        prGreen('L:')
        if not self.long_suits:
            print('', None, end='\t')
        else:
            print('', end=' ')
            for suit in self.long_suits:
                if suit == SPADE or suit == CLUB:
                    prBlack(suit)
                else:
                    prRed(suit)
            print('', end='\t')

        # Print short suits or None
        prGreen('S:')
        if not self.short_suits:
            print('', None, end='\t')
        else:
            print('', end=' ')
            for suit in self.short_suits:
                if suit == SPADE or suit == CLUB:
                    prBlack(suit)
                else:
                    prRed(suit)
            print('', end='\t')

        # Print void suits or None
        prGreen('V:')
        if not self.void_suits:
            print('', None, end='')
        else:
            print('', end=' ')
            for suit in self.void_suits:
                if suit == SPADE or suit == CLUB:
                    prBlack(suit)
                else:
                    prRed(suit)
            print('', end='')

        print('')

    def clear_hand(self):
        # Simply clears the hand
        self.hand.clear()

    def clear_book(self):
        # Simply clears the book (in case you ever want to do this)
        self.book.clear()

    def clear_suit_counts(self):
        # Clears both the list and dict used for counting suits
        for suit in SUITS:
            self.suit_count.update({suit: 0})
        self.long_suits.clear()
        self.short_suits.clear()
        self.void_suits.clear()

    def clear_all(self):
        # Clears current hand, working_hand, book, and various Player stats
        self.clear_hand()
        self.clear_book()
        self.working_hand.clear()
        self.points_in_hand = 0
        self.clear_suit_counts()


# Create cards
class Card:
    def __init__(self, suit=SUITS[0], rank=RANKS[0], points=0, status=None):
        self.suit = suit
        self.rank = rank
        self.points = points
        self.status = status

    def __str__(self):
        return "{}{}".format(self.suit, self.rank)

    def __repr__(self):
        return {"suit": self.suit, "rank": self.rank}

    def __eq__(self, other):
        if self.suit == other.suit and self.rank == other.rank:
            return True
        return False

    def __lt__(self, other):
        if self.suit == other.suit:
            if self.rank == 'A':
                return False
            elif self.rank == 'K':
                if other.rank == 'A':
                    return True
                else:
                    return False
            elif self.rank == 'Q':
                if other.rank == 'K' or other.rank == 'A':
                    return True
                else:
                    return False
            elif self.rank == 'J':
                if other.rank == 'Q' or other.rank == 'K' or other.rank == 'A':
                    return True
                else:
                    return False
            elif self.rank == 'T':
                if other.rank == 'J' or other.rank == 'Q' or other.rank == 'K' or other.rank == 'A':
                    return True
                else:
                    return False
            elif other.rank == 'T' or other.rank == 'J' or other.rank == 'Q' or other.rank == 'K' or other.rank == 'A':
                return True
            else:
                return int(self.rank) < int(other.rank)
        elif self.suit == SUITS[0]:
            return True
        elif other.suit == SUITS[0]:
            return False
        elif self.suit == SUITS[3]:
            return False
        elif other.suit == SUITS[3]:
            return True
        elif self.suit == SUITS[2]:
            return False
        else:
            return True

    def __le__(self, other):
        if self.suit == other.suit:  # unsure if this case is important for cards
            return True
        elif self.suit == SUITS[0]:
            return True
        elif other.suit == SUITS[0]:
            return False
        elif self.suit == SUITS[3]:
            return False
        elif other.suit == SUITS[3]:
            return True
        elif self.suit == SUITS[2]:
            return False
        else:
            return True

    def __gt__(self, other):
        if self.suit == other.suit:
            if self.rank == 'A':
                return True
            elif self.rank == 'K':
                if other.rank == 'A':
                    return False
                else:
                    return True
            elif self.rank == 'Q':
                if other.rank == 'K' or other.rank == 'A':
                    return False
                else:
                    return True
            elif self.rank == 'J':
                if other.rank == 'Q' or other.rank == 'K' or other.rank == 'A':
                    return False
                else:
                    return True
            elif self.rank == 'T':
                if other.rank == 'J' or other.rank == 'Q' or other.rank == 'K' or other.rank == 'A':
                    return False
                else:
                    return True
            elif other.rank == 'T' or other.rank == 'J' or other.rank == 'Q' or other.rank == 'K' or other.rank == 'A':
                return False
            else:
                return int(self.rank) > int(other.rank)
        elif self.suit == SUITS[0]:
            return False
        elif other.suit == SUITS[0]:
            return True
        elif self.suit == SUITS[3]:
            return True
        elif other.suit == SUITS[3]:
            return False
        elif self.suit == SUITS[2]:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.suit == other.suit:
            return True
        elif self.suit == SUITS[0]:
            return False
        elif other.suit == SUITS[0]:
            return True
        elif self.suit == SUITS[3]:
            return True
        elif other.suit == SUITS[3]:
            return False
        elif self.suit == SUITS[2]:
            return True
        else:
            return False

    def print_status(self):
        if self.status == OUT:
            prBlue(self)
            print('', end=' ')
        elif self.status == SAFE:
            prGreen(self)
            print('', end=' ')
        elif self.status == UNSAFE:
            prRed(self)
            print('', end=' ')
        else:
            prBlack(self)
            print('', end=' ')
        # print('')

    def clear_status(self):
        # Clears self.status
        self.status = None


def gather_game_data():
    # Asks user for game data and returns the info necessary to build the game in a tuple.
    num_humans = 5
    num_ai = 4
    list_of_names = []
    list_of_ai_types = []
    ai_notes_input = ''
    ai_notes = False
    ai_wh = False

    # Asks for humans and their names.
    while int(num_humans) < 0 or int(num_humans) > 4:
        num_humans = input('How many human players?')                   # get the number of human players
        print('')

    for human in range(0, int(num_humans)):                             # make space in name list
        list_of_names.append('')

    for human_ind in range(0, int(num_humans)):                         # get name from user and add to list
        print('Please name human number', (human_ind + 1), end='')
        name_input = input(': ')
        list_of_names[human_ind] = name_input
    print('')

    for human in range(0, int(num_humans)):                             # add HUMAN_AI to list of AI types
        list_of_ai_types.append(HUMAN_AI)

    # If there is an AI player, ask for AI type and other information.
    num_ai -= int(num_humans)
    if num_ai:
        print('Enter 1 for CPU_AI or 2 for RANDOM_AI')                  # ask for desired types of AI
        for ai_ind in range(0, num_ai):
            print('Please enter a number for AI', (ai_ind + 1), end='')
            ai_input = input(': ')
            if int(ai_input) == 1:
                list_of_ai_types.append(CPU_AI)
            else:
                list_of_ai_types.append(RANDOM_AI)
        print('')

        # Ask user if they'd like to see AI notes and/or their working hands to get a feel for how the AI works.
        while not (ai_notes_input == 'y' or ai_notes_input == 'Y' or ai_notes_input == 'n' or ai_notes_input == 'N'):
            print('Would you like to see AI notes? It may be interesting to clarify decisions the AI makes.')
            ai_notes_input = input('y/n:')
            print('')
        if ai_notes_input == 'y' or ai_notes_input == 'Y':
            ai_notes = True

            ai_notes_input = ''
            while not (ai_notes_input == 'y' or ai_notes_input == 'Y' or
                       ai_notes_input == 'n' or ai_notes_input == 'N'):
                print("Would you like to see AI working hands? (It's pretty cool!)")
                ai_notes_input = input('y/n:')
            if ai_notes_input == 'y' or ai_notes_input == 'Y':
                ai_wh = True
                print("\nYou'll see the AI's 'working' hand color-coded by card status.")
                prBlue('Blue')
                print(" = it's an 'out', meaning it's guaranteed to not take a trick")
                prGreen('Green')
                print(" = it's safe, meaning it could result in taking a zero-point trick")
                prRed('Red')
                print(" = it's unsafe, meaning it could result in taking a point trick")
                input('[ENTER]')
            print('')

    # If there are humans, print instructions
    if int(num_humans):
        print("Instructions:")
        print("If you aren't familiar with Hearts, try this video: https://www.youtube.com/watch?v=3Pj7y_vOs7Q")
        print("\tNOTE: Passing before beginning a hand isn't implemented yet!")
        print("To play a card, the game accepts only two-character input. Either:")
        print("\t-Suit followed by Rank (i.e. C2 for the 2 of clubs)")
        print("\t-Rank followed by Suit (i.e. TH for the 10 of hearts)")
        print("Aside from the 10 being entered as T, the others should be self-explanatory.")
        print("The game will assume you know this and simply ask again if you give it invalid input!")
        print('\nGood luck!')

    # Finish filling out the list of names with numbered CPUs!
    cpu_num = 1
    while len(list_of_names) < 4:
        cpu_name = 'CPU {}'.format(cpu_num)
        list_of_names.append(cpu_name)
        cpu_num += 1

    input('[ENTER]')
    print('\n')

    return (list_of_names[0], list_of_names[1], list_of_names[2], list_of_names[3],
            list_of_ai_types[0], list_of_ai_types[1], list_of_ai_types[2], list_of_ai_types[3], ai_notes, ai_wh,
            num_humans, num_ai)


# START HERE: Print info!
print('\n\nWELCOME TO:')
print('Another Basic Hearts Engine')
print('By Donny Ebel')
print('MTH 205')
print('Fall 2021', end='\n\n')
print('Credits:')
print('https://www.geeksforgeeks.org/print-colors-python-terminal/ for help with color printing!')
print('http://mark.random-article.com/hearts/terms.html for helpful terminology to think about the game differently!')
print("https://sites.ualberta.ca/~amw8/hearts.pdf for inspiration and thoughts on what can/can't be done!", end='\n\n')

# Ask user for game info, make the game, then play it!
game_data = gather_game_data()

Hearts = Game(game_data[0], game_data[1], game_data[2], game_data[3],
              game_data[4], game_data[5], game_data[6], game_data[7],
              game_data[8], game_data[9], game_data[10], game_data[11])

Hearts.play_the_game()

# Maybe add 'Would you like to keep going?' prompt after each hand.
# Maybe print the ai type at the bottom of CPU players?
