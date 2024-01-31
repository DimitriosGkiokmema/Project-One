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
    p = Player(0, 0)  # set starting location of player; you may change the x, y coordinates here as appropriate

    menu = ["look", "inventory", "score", "quit", "back"]

        while not p.victory:
        location = w.get_location(p.x, p.y)

        # prints either full description (first time visit) or brief description (every subsequent visit)
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)

        # No matter what location this is, since we visited it .visited is now true
        location.visited = True

        print("What to do? \n")
        print("[menu]")
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
        elif choice == 'inventory':
            pass  # TODO: CREATE FUNCTION FOR THIS
        elif choice == 'score':
            pass  # TODO: CREATE FUNCTION FOR THIS
        elif choice == 'quit':
            pass  # TODO: CREATE FUNCTION FOR THIS
        elif choice == 'back':
            pass  # TODO: CREATE FUNCTION FOR THIS
        elif choice in location.available_directions:
            p.update(choice)
        elif choice in ['East', 'North', 'South', 'West']:  # Direction not allowed
            print(w.get_location(1, 0).long_description)
        else:  # Only occurs if choice is not any of the options
            print('\nNot an action!!!')

        print('')

        #  Possibilities:
        #  A helper function such as do_action(w, p, location, choice)
        #  OR A method in World class w.do_action(p, location, choice)
        #  OR Check what type of action it is, then modify only player or location accordingly
        #  OR Method in Player class for move or updating inventory
        #  OR Method in Location class for updating location item info, or other location data etc....
