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
        - self.name != ""
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
        """

        # NOTES:
        # This is just a suggested starter class for Item.
        # You may change these parameters and the data available for each Item object as you see fit.
        # (The current parameters correspond to the example in the handout).
        # Consider every method in this Item class as a "suggested method".
        #
        # The only thing you must NOT change is the name of this class: Item.
        # All item objects in your game MUST be represented as an instance of this class.

        self.name = name
        self.start_position = start
        self.target_position = target
        self.target_points = target_points

    def __str__(self) -> str:
        """Return a string representation of the item.
        """
        return (
            f"{self.name} - Start: {self.start_position}, "
            f"Target: {self.target_position}, Points: {self.target_points}"
        )
    
    
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

    def __init__(self, position: tuple[int, int], brief_description: str, long_description: str,
                 available_directions: list[str], items: list[Item] = None) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        # NOTES:
        # Data that could be associated with each Location object:
        # a position in the world map,
        # a brief description,
        # a long description,
        # a list of available commands/directions to move,
        # items that are available in the location,
        # and whether the location has been visited before.
        # Store these as you see fit, using appropriate data types.
        #
        # This is just a suggested starter class for Location.
        # You may change/add parameters and the data available for each Location object as you see fit.
        #
        # The only thing you must NOT change is the name of this class: Location.
        # All locations in your game MUST be represented as an instance of this class.

        self.position = position
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_directions = available_directions
        self.items = [] if items is None else items
        self.visited = False

    def available_actions(self) -> list[str]:
        """
        Return the available actions in this location.
        The actions should depend on the items available in the location
        and the x,y position of this location on the world map.
        """

        # NOTE: This is just a suggested method
        # i.e. You may remove/modify/rename this as you like, and complete the
        # function header (e.g. add in parameters, complete the type contract) as needed

        actions = []

        # Check if the location has items
        if self.items:
            actions.append("Pick up items")

        # Check if the player has the required items for the exam
        required_items = {'T-card', 'Cheat Sheet', 'Lucky Pen'}
        player_items = {item.name for item in self.items}

        if all(item in player_items for item in required_items):
            actions.append("Take the exam")

        return actions


class Player:
    """
    A Player in the text advanture game.

    Instance Attributes:
        - # TODO

    Representation Invariants:
        - # TODO
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initializes a new Player at position (x, y).
        """

        # NOTES:
        # This is a suggested starter class for Player.
        # You may change these parameters and the data available for the Player object as you see fit.

        self.x = x
        self.y = y
        self.inventory = []
        self.victory = False


class World:
    """A text adventure game world storing all location, item and map data.

    Instance Attributes:
        - map: a nested list representation of this world's map

    Representation Invariants:
        - map contains only location numbers and -1
    """
    map: list[list[int]]

    def __init__(self, map_data: TextIO, location_data: TextIO, items_data: TextIO) -> None:
        """
        Initialize a new World for a text adventure game, based on the data in the given open files.

        - location_data: name of text file containing location data (format left up to you)
        - items_data: name of text file containing item data (format left up to you)
        """

        # NOTES:

        # map_data should refer to an open text file containing map data in a grid format, with integers separated by a
        # space, representing each location, as described in the project handout. Each integer represents a different
        # location, and -1 represents an invalid, inaccessible space.

        # You may ADD parameters/attributes/methods to this class as you see fit.
        # BUT DO NOT RENAME OR REMOVE ANY EXISTING METHODS/ATTRIBUTES IN THIS CLASS

        # The map MUST be stored in a nested list as described in the load_map() function's docstring below
        self.map = self.load_map(map_data)

        # NOTE: You may choose how to store location and item data; create your own World methods to handle these
        # accordingly. The only requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

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
        >>> world.load_map(open("map.txt"))
        [[5, -1, -1, 8, 9], [4, 3, 1, 7, -1], [6, -1, 2, -1, -1]]
        """
        map_list = map_data.readlines()

        # put each number into different indexes in the list
        for i in range(len(map_list)):
            map_list[i] = map_list[i].split()

        # convert each num from str to int
        map_list = [[int(i) for i in lst] for lst in map_list]

        return map_list

    # TODO: Add methods for loading location data and item data (see note above).
    def load_locations(self, places: TextIO) -> None:
        """
        Create all the Location objects and store them in a list

        /position: tuple[int, int]
        brief_description: str
        /long_description: str
        /available_directions: list[str]
        /items: list[Item]
        visited: bool
        """
        locations = places.readlines()
        long_description = []
        description = ''

        # Fill list with descriptions for the locations, except for LOCATION -1
        for line in locations:
            if line == '\n':
                long_description.append(description)
                description = ''
            else:
                description = description + line

        # Find positions of locations on map
        positions = []

        for num in range(1, 10):
            for r in range(len(self.map)):
                for c in range(len(self.map[r])):
                    if self.map[r][c] == num:
                        positions.append((r, c))

        # Get available directions
        directions = []

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

        # Find location of items and create new Item objects
        item_file = open('items.txt').readlines()
        item_file.sort()
        items = []

        for i in range(len(item_file)):
            item_file[i] = item_file[i].split()

        for item in range(len(item_file)):
            start = int(item_file[item][0])
            target = int(item_file[item][1])
            points = int(item_file[item][2])
            name = item_file[item][3]

            items.append(Item(name, start, target, points))

        # STILL UNDER CONSTRUCTION

    # NOTE: The method below is REQUIRED. Complete it exactly as specified.
    def get_location(self, x: int, y: int) -> Optional[Location]:
        """Return Location object associated with the coordinates (x, y) in the world map, if a valid location exists at
         that position. Otherwise, return None. (Remember, locations represented by the number -1 on the map should
         return None.)

         >>> world = World(open("map.txt"), open("locations.txt"), open("items.txt"))
        >>> world.get_location(open("locations.txt"))
        """
        num = self.map[x][y]

        if num == -1:
            return None
