"""CSC111 Project 1: Text Adventure Game Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the main classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2024 CSC111 Teaching Team
"""
from typing import Optional, TextIO


class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - name: a string representing the name of the item
        - start_position: an integer representing the initial location of the item
        - target_position: an integer representing the target location where the item should be deposited for credit
        - target_points: an integer representing the points received for depositing the item in the target location


    Representation Invariants:
        - isinstance(self.name, str) and self.name != ""
        - self.start_position >= 0
        - self.target_position >= 0
        - self.target_points >= 0
    """
    name: str
    start_position: int
    target_position: int
    target_points: int

    def __init__(self, name: str, start: int, target: int, target_points: int) -> None:
        """Initialize a new item.
        >>> item = Item('shield', 1, 5, 500)
        >>> item.name == 'shield'
        True
        """
        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points

class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - position: A tuple representing the (x, y) position on the map
        - brief_description: A brief description of the location
        - long_description: A longer description shown only the first time the location is visited
        - available_directions: A list of available directions to move from this location
        - items: A list of items available in the location
        - visited: A boolean indicating whether the location has been visited before

    Representation Invariants:
         - 0 <= self.position[0] <= 9 and 0 <= self.position[1] <= 9
    """
    position: tuple[int, int]
    brief_description: str
    long_description: str
    available_directions: list[str]
    items: list[Item]
    visited: bool

    def __init__(self, position: tuple[int, int], long_description: str,
                 available_directions: list[str], items: list[Item]) -> None:
        """Initialize a new location.
        >>> l = Location((1,1), 'long', ['East'], [])
        >>> l.available_directions[0] == 'East'
        True
        """
        self.position = position
        self.brief_description = self.short_descriptions(long_description)
        self.long_description = long_description
        self.available_directions = available_directions
        self.items = items
        self.visited = False

    def short_descriptions(self, long: str) -> str:
        """
        Returns a list of shorts description for each location
        The descriptions for the locations begin by describing nearby places and then describe your current location
        This function simply creates a list of the location descriptions up to the nearby places. The description for
        the current place is not included

        >>> shield = Item('shield', 1, 5, 500)
        >>> l = Location((1,1), 'Innis is North of Robarts', ['East'], [shield])
        >>> 'Innis is North' in l.brief_description
        True
        """
        word_len = 0
        max_index = 0

        for i in ['East', 'West', 'South', 'North']:
            if i in long and long.index(i) > max_index:
                max_index = long.index(i)
                word_len = len(i)

        if max_index == 0:  # Ensures that if no direction is in description, brief_description == long_description
            max_index = len(long) - 1

        return long[: max_index + word_len + 1] + '\nEND'

    def available_actions(self) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.

        If an item exists, add 'Pick up items' in actions and return it
        >>> shield = Item('shield', 1, 5, 500)
        >>> l = Location((1,1), 'long', ['East'], [shield])
        >>> l.available_actions()[0] == 'Pick up items'
        True
        >>> l = Location((1,1), 'long', ['East'], [])
        >>> len(l.available_actions()) == 0
        True
        """
        actions = []

        # Check if the location has items
        if self.items:
            actions.append("Pick up items")

        return actions


class PuzzleLocation(Location):
    """A location in our text adventure game world with an additional puzzle.

    Instance Attributes:
        - puzzle_code: An optional passcode required to solve the puzzle in this location.

    Representation Invariants:
        - (self.puzzle_code is None) or type(self.puzzle_code) == int
    """
    puzzle_code: Optional[int]

    def __init__(self, position: tuple[int, int], long_description: str, puzzle_code: Optional[int] = None) -> None:
        """Initialize a new location with a puzzle.

        If puzzle_code is not None, the player needs to enter this code to solve the puzzle.
        """
        # sends values to the parent class (Location)
        super().__init__(position, long_description, [], [])
        self.puzzle_code = puzzle_code

    def solve_puzzle(self, attempts: int, max_attempts: int = 6) -> bool:
        """Attempt to solve the puzzle in the given PuzzleLocation.
        The numbers to the code are hidden in the location descriptions
        "1 is drawn in red paint"
        "4 students are studying"
        "A new item costs $6"
        There are only six combinations of these numbers, so the player should get the puzzle right eventually
        However, if the player does not guess 416 (the code) within six tries, there is no way to do the puzzle
        again and the game must restart

        This function cannot have doctests as the player needs to type the code, however here are some scenarios:
        attempt 1: player types 614
        Incorrect passcode. Try again!

        attempt 2: player types 641
        Incorrect passcode. Try again!

        attempt 3: player types 146
        Incorrect passcode. Try again!

        attempt 4: player types 164
        Incorrect passcode. Try again!

        attempt 5: player types 461
        Incorrect passcode. Try again!

        attempt 6: player types 416
        You successfully solved the puzzle at location {self.position}!
        """
        if attempts < max_attempts:
            passcode = input('Enter the three digit code for the safe.\nNote that the code only contains numbers: ')
            attempts += 1

            if int(passcode) == self.puzzle_code:
                print(f"You successfully solved the puzzle at location {self.position}!")
                return True
            else:
                print("Incorrect passcode. Try again!")
                return False
        else:
            print(f"Sorry, you've reached the maximum number of attempts ({max_attempts}). Puzzle unsolved.")
            return False


class Player:
    """
    A Player in the text adventure game.

    Instance Attributes:
        - x and y are the coordinates of the player in the map
        - inventory keeps track of items picked up
        - victory turns true when player has all items in inventory
        - score keeps track of the player's score

    Representation Invariants:
        - 0 <= x < width of map
        - 0 <= y < length of map
        - inventory holds only Items
        - victory only true when all items are found and deposited at the correct locations
        - score >= 0
    """
    x: int
    y: int
    inventory: list[Item]
    victory: bool
    score: int = 0

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """
        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False

    def update(self, direction: str) -> bool:
        """ Updates the player position if a valid direction is inputed
        Valid directions vary among locations

        >>> shield = Item('shield', 1, 5, 500)
        >>> l = Location((1,1), 'long', ['East'], [shield])
        >>> p = Player(4, 4)
        >>> p.update('Go East')
        True
        >>> p.update('Go East')
        False
        """
        map_width = 5
        map_length = 5

        if direction == 'Go East' and self.x < map_width:
            self.x += 1
        elif direction == 'Go West' and self.x > 0:
            self.x -= 1
        elif direction == 'Go North' and self.y > 0:
            self.y -= 1
        elif direction == 'Go South' and self.y < map_length:
            self.y += 1
        else:
            return False

        return True

    def pick_up_item(self, location: Location, item: Item) -> None:
        """
        Pick up items available in the current location and add them to the player's inventory.

        >>> shield = Item('shield', 1, 5, 500)
        >>> l = Location((1,1), 'long', ['East'], [shield])
        >>> p = Player(1, 1)
        >>> p.score
        0
        >>> p.pick_up_item(l, shield)
        You pick up shield.
        >>> p.score
        5
        """
        print(f"You pick up {item.name}.")
        self.score += 5

        if self.inventory:
            self.inventory.append(item)
        else:
            self.inventory = [item]

        location.items = [i for i in location.items if i != item]

    def drop_items(self, location: Location, choice: str, objectives: dict[str, bool]) -> bool:
        """ Allows player to drop items in the current location
        Checks if item is being deposited at a location that it is an OBJECTIVE of (read location.txt)
        Prints if was successful and returns True. If not, prints 'Not a valid choice!' and returns False

        >>> objective = {'T_Card': False, 'Lucky_Pen': False, 'Backpack': False, 'Cheat_Sheet': False}
        >>> card = Item('T_Card', 1, 5, 500)
        >>> l = Location((1,1), 'long', ['East'], [card])
        >>> p = Player(1, 1)
        >>> p.pick_up_item(l, card)
        You pick up T_Card.
        >>> p.drop_items(l, "T_Card", objective)
        You dropped  T_Card
        True
        """
        index = self.find_item_index(self.inventory, choice)

        if index != -1:
            item = self.inventory.pop(self.find_item_index(self.inventory, choice))
            location.items.append(item)
            print('You dropped ', item.name)

            for i in objectives:
                if i in location.long_description:
                    objectives[i] = True
                    self.score += 5

            return True
        else:
            print('Not a valid choice!')
            return False

    def find_item_index(self, lst: list[Item], choice: str) -> int:
        """
        The player enters the name of the item that is to be dropped.
        This function finds the index of said item in a collection
        of items (either self.inventory or location.items).
        Returns -1 if target item not in list

        >>> card = Item('T_Card', 1, 5, 500)
        >>> l = Location((1,1), 'long', ['East'], [card])
        >>> p = Player(1, 1)
        >>> p.pick_up_item(l, card)
        You pick up T_Card.
        >>> p.find_item_index(p.inventory, "T_Card")
        0
        """
        for i in range(len(lst)):
            if lst[i].name == choice:
                return i
        return -1


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map
        - locations: a list containing all the location objects
        - items: holds all Item objects

    Representation Invariants:
        - map contains only location numbers and -1
    """
    map: list[list[int]]
    locations: list[Location]
    items: list[Item]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """
        self.map = self.load_map(map_data)  # Creates map
        self.items = []
        self.load_items(items_data)  # Fills item list
        self.locations = []
        self.load_locations(location_data)  # Fills locations list

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def load_map(self, map_data: TextIO) -> list[list[int]]:
        """
        Store map from open file map_data as the map attribute of this object, as a nested list of integers like so:

        If map_data is a file containing the following text:
            1 2 5
            3 -1 4
        then load_map should assign this World object's map to be [[1, 2, 5], [3, -1, 4]].

        Return this list representation of the map.
        >>> world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
        >>> world.map
        [[5, -1, -1, 8, 9], [4, 3, 1, 7, -1], [6, -1, 2, -1, -1]]
        """
        map_list = map_data.readlines()

        # put each number into different indexes in the list
        for i in range(len(map_list)):
            map_list[i] = map_list[i].split()

        # convert each num from str to int
        map_list = [[int(num) for num in lst] for lst in map_list]

        return map_list

    def load_items(self, item_file: TextIO) -> None:
        """
        Create Item objects and store them in self.items
        Please note that this doctest underlines item and highlights name
        Even though the test and function both work PyCharm is showing errors
        We did not know how to fix them, and as the code works, we ignored them
        Hopefully this is not a big deal!

        >>> world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
        >>> [item.name for item in world.items]
        ['T_Card', 'Cheat_Sheet', 'Lucky_Pen', 'Backpack']
        """
        # Find location of items and create Item objects
        item_file = item_file.readlines()

        for i in range(len(item_file)):
            item_file[i] = item_file[i].split()

        for item in item_file:
            start = int(item[0])
            target = int(item[1])
            points = int(item[2])
            name = item[3]

            self.items.append(Item(name, start, target, points))

    def load_locations(self, places: TextIO) -> None:
        """
        Create all the Location objects and store them in a list
        Additionally, create a list storing all item objects in the game
        What this function does is create lists of every variable needed to create a location object
        i.e. brief and long descriptions, position, available directions and items.
        Then, it goes through each list, takes the value at list[index] of each list, and creates the location
        All the locations are stored in world.locations

        >>> world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
        >>> print(world.locations[8].brief_description)
        LOCATION 9
        OBJECTIVE: Cheat_Sheet
        You are under a tree by the entrance of Innis College. The entrance to Innis is to the West.
        END
        """
        location_file = places.readlines()
        long_description = []
        description = ''

        # Fill list with descriptions for the locations 1-9
        for line in location_file:
            if line == '\n':
                long_description.append(description)
                description = ''
            else:
                description = description + line
        long_description.append(description)  # adds location -1

        # Find positions of locations on map
        positions = []

        for num in range(1, 10):
            self.get_location_position(num, positions)

        # Get available directions
        directions = []
        self.get_directions(long_description, directions)

        # Create Location objects for each location (except LOCATION -1 and 10)
        for i in range(9):
            new_item = []

            for item in self.items:
                if item.start_position == i + 1:
                    new_item.append(item)

            place = Location(positions[i], long_description[i], directions[i], new_item)
            self.locations.append(place)

        # Add location for LOCATION -1
        # anytime player goes out of bounds, LOCATION -1 is displayed
        # remember that the description of location -1 was the last one added
        dead_end = long_description[len(long_description) - 1]
        self.locations.append(Location((0, 1), dead_end, [], []))

    def get_location_position(self, num: int, positions: list[tuple[int, int]]) -> None:
        """ Finds the position of a number in the map. Each number represents a location.
        The position of these numbers are saved as tuples in the positions list

        >>> world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
        >>> pos = []
        >>> world.get_location_position(3, pos)
        >>> pos
        [(1, 1)]
        """
        for r in range(len(self.map)):
            for c in range(len(self.map[r])):
                if self.map[r][c] == num:
                    positions.append((r, c))

    def get_directions(self, long_description: list[str], directions: list[list[str]]) -> None:
        """
        Fills a list with the direction available at each location by searching for them in its description

        >>> world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
        >>> correct_directions = {'South', 'West', 'East'}
        >>> set(world.locations[0].available_directions) == correct_directions
        True
        """
        # Checks what directions are mentioned in the description and adds them to directions
        for location in long_description:
            lst = []

            if 'East' in location:
                lst.append('East')
            if 'South' in location:
                lst.append('South')
            if 'West' in location:
                lst.append('West')
            if 'North' in location:
                lst.append('North')

            directions.append(lst)

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Location:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)

        >>> world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
        >>> 'LOCATION 5' in world.get_location(0, 0).long_description
        True
        """
        if x < len(self.map[0]) and y < len(self.map):
            location_num = self.map[y][x]

            if location_num == -1:
                return self.locations[9]
            else:
                return self.locations[location_num - 1]
        else:
            return self.locations[9]


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
