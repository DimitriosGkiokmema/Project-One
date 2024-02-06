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
from game_data import World, Player, PuzzleLocation

if __name__ == "__main__":
    with open('map.txt') as map_file, open('locations.txt') as location_file, open('items.txt') as item_file:
        w = World(map_file, location_file, item_file)
    p = Player(2, 1)  # set starting location of player; you may change the x, y coordinates here as appropriate
    safe = w.get_location(1, 1)  # set puzzle variable
    safe_long = safe.long_description
    safe = PuzzleLocation(safe.position, safe_long, 416)
    safe_crack_attempts = 0
    quit_game = False
    cracked_safe = False
    num_moves = 20
    last_move = ''
    menu = ["look", "inventory", "score", "quit", "back"]
    # objectives represents which items have been deposited at the correct locations.
    # The player can only win if all values in this variable are True
    objectives = {'T_Card': False, 'Lucky_Pen': False, 'Backpack': False, 'Cheat_Sheet': False}
    deposit = {'T_Card': 'Robarts entrance', 'Lucky_Pen': 'study room', 'Backpack': 'Starbucks',
               'Cheat_Sheet': 'tree by Innis'}

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

    """ The game loop only stops when the player runs out of moves or when the player deposited all items in the
    correct locations AND solved the puzzle. What this loop basically does is ask the player to type an action and then
    performs the action. So if the player wants to go East, the player's x value is incremented by one. If the player
    wants to pick up an item, player.pick_up_item() is called. Basically the program asks the player for an action,
    interprets it, and then calls other functions to make it happen through conditionals. Think of our adventure.py
    as the CPU of our game; it controls everything and makes sure the game is running as expected.
    """
    while not p.victory and not quit_game and num_moves > 0:
        location = w.get_location(p.x, p.y)

        # prints either full description (first time visit) or brief description (every subsequent visit)
        if location.visited:
            print(location.brief_description)
        else:
            print(location.long_description)

        # If the player is in LOCATION 2 (where the safe is found), a new action is shown to the player - 'open safe'
        if 'safe' in location.long_description:
            menu = ["look", "inventory", "score", "quit", "back", 'open safe']
        else:
            menu = ["look", "inventory", "score", "quit", "back"]

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
            # since what description is printed (brief/long) depends on location.visited, we
            # simply set it to false for it to print the full description
            location.visited = False
        elif choice == 'Inventory':
            choice = input('\nTo view items in your inventory, enter view.\nTo drop items, enter drop\nYour choice: ')
            inventory_items = [element.name for element in p.inventory]

            if len(p.inventory) == 0:
                print('No items in your inventory!!!')
            elif choice == 'view':
                print(inventory_items)
            elif choice == 'drop':
                choice = input(f'Your inventory has {inventory_items}\nWhich item do you want to drop: ')
                if p.drop_items(location, choice, objectives):
                    last_move = 'Dropped ' + choice
            else:
                print('Not a valid choice!')

        elif choice == 'Score':
            print('Your current score is ', p.score)
        elif choice == 'Quit':  # Only way for the player to stop the game without brute forcing the run to stop
            quit_game = True
        elif choice == 'Open Safe' and 'open safe' in menu:
            if not cracked_safe:
                if safe.solve_puzzle(safe_crack_attempts):
                    # Player successfully solved the puzzle, not able to replay the puzzle
                    cracked_safe = True
                    safe_crack_attempts += 1
                    p.score += 15
                num_moves -= 1
            else:
                print('You already solved the puzzle and opened the safe!!!')
        elif choice == 'Objectives':
            # Prints the deposit locations of all items not already in the correct deposit location
            # This way, the player is reminded of the game's goals and is not wasting their num_moves count
            for objective in objectives:
                if not objectives[objective]:
                    print(f'The {objective} needs to be deposited at the {deposit[objective]}')
            print('You need to find a code to open the safe!!!')
        elif choice == 'Pick Up Items':
            if location.available_actions() and location.available_actions()[0] == 'Pick up items':
                # If player is able to pick up the items, all are picked up
                # If you drop an item and pick up the items in the location, you also pick up the dropped item!!!
                items_to_pick_up = [i for i in location.items if i not in p.inventory]

                for item in items_to_pick_up:
                    p.pick_up_item(location, item)
                    last_move = 'picked up ' + item.name
            else:
                print('No items to pick up!!!')
        elif any(direction in choice for direction in location.available_directions):
            # Player entered correct direction, coordinates and location are changing
            if p.update(choice):
                num_moves -= 1
                last_move = choice
        elif choice == 'Back':
            num_moves += 1
            item = ''
            # this variable stores a str description of the last action taken by the player
            # to decipher it, the program looks at the last word in the variable (it is always an action) and negates it
            if last_move != '':
                item = last_move.split()
                item = item[len(item) - 1]

            if 'picked up' in last_move:  # If the player picked up an item, drop it
                p.drop_items(location, item, objectives)
            elif 'dropped' in last_move:  # If player dropped an item, pick it up
                p.pick_up_item(location, location.items[len(location.items) - 1])
            elif 'Go' in last_move:  # Player goes back to last location
                opposite_direction = {'East': 'West', 'West': 'East', 'North': 'South',
                                      'South': 'North'}
                p.update('Go ' + opposite_direction[last_move])
            else:
                print('There is no previous move recorded to go back to!')
        elif choice in ['Go East', 'Go North', 'Go South', 'Go West']:  # Direction not allowed, prints LOCATION -1
            description = w.get_location(1, 0).long_description
            print(description)
        else:  # Only occurs if choice is not any of the options or if direction without 'Go ' was entered
            print('\nNot an action!!!')
            if choice in ['East', 'West', 'South', 'North']:
                print('To move around, enter direction in the format: Go [direction]')

        if all(objectives[mission] is True for mission in objectives):
            p.victory = True

        print('')

    if p.victory and cracked_safe:  # Player is victorious
        print('Congratulations! You found all items and cracked the safe!\nYou got to the Exam Room on time.')
        print('You won the game!!!')
    elif p.victory:  # Semi win, did not solve puzzle!
        print('You found all items but could not open the safe\\nGAME OVER')
    else:  # Means the player wanted to quit the game or no moves left
        print('Ran out of moves!\nGAME OVER')

if __name__ == '__main__':
    # Uncomment to test
    # import doctest
    # doctest.testmod(verbose=True)
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
