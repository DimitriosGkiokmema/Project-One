"""CSC111 Project 1: Text Adventure Game

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""

# Note: You may add in other import statements here as needed
from game_data import World, Item, Location, Player

# Note: You may add helper functions, classes, etc. here as needed

# Note: You may modify the code below as needed; the following starter template are just suggestions
if __name__ == "__main__":
    w = World(open("map.txt"), open("locations.txt"), open("items.txt"))
    p = Player(2, 1)  # set starting location of player; you may change the x, y coordinates here as appropriate
    quit_game = False
    num_moves = 15

    menu = ["look", "inventory", "score", "quit", "back"]

    s = ('You\'ve got an important exam coming up this evening, and you\'ve been studying for weeks. Last night was a\n'
         'particularly late night on campus. You had difficulty focusing, so rather than staying in one place, you\n'
         'studied in various places throughout campus as the night progressed. Unfortunately, when you woke up this\n'
         'morning, you were missing some important exam-related items. You cannot find your T-card, and you\'re\n'
         'nervous they won\'t let you into tonight\'s exam without it. Also, you seem to have misplaced your lucky\n'
         'exam pen -- even if they let you in, you can\'t possibly write with another pen! Your backpack is nowhere\n'
         'to be seen, it has your most valuable things, like your laptop and more importantly, your lunch! Finally\n'
         'your instructor for the course lets you bring a cheat sheet - a handwritten page of information in the exam\n'
         'Last night, you painstakingly crammed as much material onto a single page as humanly possible, but that\'s\n'
         'missing, too! All of this stuff must be around campus somewhere! Can you find all of it before your exam '
         'starts tonight?\n\n')
    print('\n\n' + s)

    while not p.victory and not quit_game and num_moves > 0:
        location = w.get_location(p.x, p.y)

        # prints either full description (first time visit) or brief description (every subsequent visit)
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)

        # No matter what location this is, since we visited it .visited is now true
        location.visited = True

        print("What to do? \n")
        print("[menu]\n")
        print('Moves remaining: ', num_moves)
        for action in location.available_actions():
            print(action)
        choice = input("\nEnter action: ")

        if choice == "[menu]":
            print("Menu Options: \n")
            for option in menu:
                print(option)
            choice = input("\nChoose action: ")

        choice = choice.title()

        if choice == 'Look':
            location.visited = False
        elif choice == 'Inventory':
            if len(p.inventory) == 0:
                print('No items in your inventory!!!')
            else:
                print([item.name for item in p.inventory])
        elif choice == 'Score':
            print('Your current score is ', p.score)
        elif choice == 'Quit':
            quit_game = True
        elif choice == 'Back':
            pass  # TODO: CREATE FUNCTION FOR THIS
        elif choice == 'Pick Up Items':
            if location.available_actions()[0] == 'Pick up items':
                p.pick_up_item(location)

                if p.found_all_items():  # Once you pick up an item, check if you have all required
                    p.victory = True
            else:
                print('No items to pick up!!!')
        elif any(direction in choice for direction in location.available_directions):
            # Player entered correct direction, coordinates and location are changing
            if p.update(choice):
                num_moves -= 1
        elif choice in ['Go East', 'Go North', 'Go South', 'Go West']:  # Direction not allowed, prints LOCATION -1
            description = w.get_location(1, 0).long_description
            print(description)
        else:  # Only occurs if choice is not any of the options or if direction without 'Go ' was entered
            print('\nNot an action!!!')
            if choice in ['East', 'West', 'South', 'North']:
                print('To move around, enter direction in the format: Go [direction]')

        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....

        """
        Things I did / to do:
        moved code above from player function
        locations.available actions sent to player class
        print items available at each location
        for the enhancements a new class is needed -> PuzzleLocation (what it do?)
        Once you pick up items, what do you do? Do you drop them off or win immediately?
        """

    if p.victory:
        print('Congratulations! You found all items and got the to Exam Room on time for your exam.\\nYou won!!!')
    else:  # Means the player wanted to quit the game
        print('GAME OVER')
