from room import Room
from item import Item
from inventory import Inventory
import re
import sys


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """

    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """

        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.items = self.load_items(f"data/{game}Items.txt")

        self.inventory = Inventory()
        self.current_room = self.rooms[1]
        self.win = 0

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a dictionary of 'id' : Room objects.
        """
        # First we parse all the data we need to create the rooms with.
        # All parsed lines of data are saved to rooms_data.
        rooms_data = []
        with open(filename, "r") as f:
            room_data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    room_data.append(line.strip())
                # A blank newline signals all data of a single room is parsed.
                else:
                    rooms_data.append(room_data)
                    room_data = []
        # Append a final time, because the files do not end on a blank newline.
        rooms_data.append(room_data)

        # Create room objects for each set of data we just parsed.
        rooms = {}
        for room_data in rooms_data:
            id = int(room_data[0])
            name = room_data[1]
            description = room_data[2]

            # Initialize a room object and put it in a dictionary with its
            # id as key.
            room = Room(id, name, description)
            rooms[id] = room

        # Add routes to each room we've created with the data from each set
        # we have parsed earlier.
        for room_data in rooms_data:
            id = int(room_data[0])
            # We split to connections into a direction and a room_id.
            connections = room_data[4:]
            connections = [connection.split() for connection in connections]
            # Here we get the current room object that we'll add routes to.
            room = rooms[id]
            for connection, target_room_id in connections:
                # Add routes
                room.add_route(connection, target_room_id)

        return rooms

    def load_items(self, filename):
        """
        Load items from filename.
        Returns a dictionary of 'room_id' : Items
        """
        rooms_items = []
        with open(filename, "r") as f:
            room_item = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    room_item.append(line.strip())
                # A blank newline signals all data of a single room is parsed.
                else:
                    rooms_items.append(room_item)
                    room_item = []
        # Append a final time, because the files do not end on a blank newline.
        rooms_items.append(room_item)

        # Create item objects for each set of data we just parsed.
        items = {}
        for item_data in rooms_items:
            name = item_data[0]
            description = item_data[1]
            id = int(item_data[2])

            # If there is already an item in the room with the same id, we add that item as an list to items
            # This only works up to two items, but is enough for the game.
            if id in items.keys():
                # We get the previous item
                previous = items[id]
                # Create new item object
                item = Item(name, description, id)
                # Insert both previous and new item to self.items
                items[id] = [previous, item]
                # Add item to room
                self.rooms[id].inventory.add(item)

            # If there is no item in the room yet: Initlialize an item object, store in in a dictionary
            # with its id as key.
            else:
                item = Item(name, description, id)
                items[id] = item
                # Add item to room inventory
                self.rooms[id].inventory.add(item)

        return items

    def take(self, item, i):
        """
        Allows to user to add items into their inventory
        """
        # Check if the room id's and item names match
        if item not in self.rooms[i].inventory.check() or self.rooms[i].id != self.current_room.id:
            print("No such item")
        else:
            # Remove item from room inventory
            self.rooms[i].inventory.remove(item)
            # Add item to adventure inventory
            # If there are multiple items in the same room this will result to true
            for key in self.items.keys():
                if type(self.items[key]) == list:
                    # We loop over all items in the list
                    for j in range(len(self.items[key])):
                        # If we find the item we add it to our inventory
                        if item in str(self.items[key][j]):
                            self.inventory.add(self.items[key][j])
                            print(f"{self.items[key][j].name} taken")
                            break
                else:
                    if item in self.items[key].name:
                        self.inventory.add(self.items[key])
                        print(f"{self.items[key].name} taken")

    def drop(self, item, i):
        """
        Allows the user to drop an item from their inventory
        """

        # Make sure the user has the item in inventory
        if item not in self.inventory.check():
            print("No such item in inventory")

        else:
            # Remove item from inventory
            self.inventory.remove(item)
            # Looking for the items poisition in self.items
            done_1 = False
            # Iterate over dictionary keys
            for key in self.items.keys():
                # Workaround for corner cases when multiple items in the same room
                if type(self.items[key]) == list:
                    # Loop over items in same room
                    for j in range(len(self.items[key])):
                        # If we find the item
                        if item == self.items[key][j].name:
                             # We use its key to append item to new room
                            self.rooms[i].inventory.add(self.items[key][j])
                            print(f"{self.items[key][j].name} dropped")
                            # Break nested for loops
                            done_1 = True
                            break

                    if done_1:
                        break

                # If its not a corner-case -> directionly look for item
                elif self.items[key].name == item:
                    # Append item
                    self.rooms[i].inventory.add(self.items[key])
                    print(f"{self.items[key].name} dropped")
                    break

    def game_over(self):
        """
        Check if the game is over.
        Returns a boolean.
        """
        # If the current room is equal to the length of all rooms this indicates that you are in the final room
        # If the forced option also returns 0 this means you have won the game
        if len(self.rooms) == int(self.current_room.id) and int(self.current_room.directions['FORCED']) == 0:
            return True

        elif "FORCED" in self.current_room.directions:
            # Special workaround for corner cases with multiple forced options
            if type(self.current_room.directions['FORCED']) == list:
                for option in self.current_room.directions["FORCED"]:
                    # Get room id
                    room_id = re.findall('\d+', option)
                    room_id = int(room_id[0])
                    # Oh dear you have died...
                    if room_id == 0:
                        return True

            # Oh dear you have died...
            elif int(self.current_room.directions['FORCED']) == 0:
                return True

            else:
                return False

        else:
            return False

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """
        # If the type returns a list that means there is a conditional movement
        if type(self.current_room.directions[direction]) is list:
            done_1 = False
            # Loop over the different options
            for option in self.current_room.directions[direction]:
                # Filter the roomd ID from string if type is list
                # This is the case when a direction has multiple options
                if type(option) == list:
                    # Loop over the options in the embedded list (e.g. [14/bird, 15/rod])
                    for option in option:
                        # Get room id from option
                        room_id = re.findall('\d+', option)
                        room_id = int(room_id[0])
                        # Return true if user has the item in inventory
                        if self.item_check(option):
                            # If we have the item we take the first option available
                            self.current_room = self.rooms[room_id]
                            # Break nested for loops
                            done_1 = True
                            break
                        # Iterate over all options and eventually end up in the last one
                        else:
                            self.current_room = self.rooms[room_id]

                    if done_1:
                        break
                # If self.current_room.directions[directions] returns a regular format e.g. a number
                else:
                    # Get room_id
                    room_id = int((re.findall('\d+', option))[0])
                    # Return true if user has the item in inventory
                    if self.item_check(option):
                        # Move room
                        self.current_room = self.rooms[room_id]
                        # Terminate loop -> take first option
                        break
                    else:
                        # Iterate over all options, eventually end up in the last one
                        self.current_room = self.rooms[room_id]

        # If there is only a single direction value proceed like the original move function
        else:
            # Get id of the next room
            room_id = int(self.current_room.directions[direction])
            # Set next room
            self.current_room = self.rooms[room_id]

    def item_check(self, option):
        """
        Checks in an item is in room options and in players inventory
        """

        # Check if there are items in inventory
        if len(self.inventory.check().keys()) > 0:
            # Iterate over items
            for item in self.inventory.items:
                # If item in inventory return true
                if item in option:
                    return True
                else:
                    pass
        # If not, return false
        else:
            False

    def forced_check(self):
        """
        Function that checks in advance if next move is going to be a forced move
        """

        while "FORCED" in self.current_room.directions.keys():
            # Show room description
            self.current_room.show_description()
            if self.game_over():
                self.game_over()
                break
            else:
                self.move("FORCED")

    def play(self):
        """
        Play an Adventure game
        """

        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")

        # Print the first description
        self.current_room.show_description()
        # If there is an item in the first room, print item
        if len(self.current_room.inventory.items) != 0:
            self.current_room.inventory.show()

        # Keep track of visited rooms
        visited_rooms = [1]

        # Prompt the user for commands until they've won the game.
        # If game_over returns True the game terminates
        while not self.game_over():
            command = input("> ")
            # Make sure commands are valid
            command = command.upper()

            if command == "HELP":
                print("You can move by typing directions such as EAST/WEST/IN/OUT. \n"
                      "QUIT quits the game.\n"
                      "HELP prints instructions for the game.\n"
                      "INVENTORY lists the item in your inventory.\n"
                      "LOOK lists the complete description of the room and its contents.\n"
                      "TAKE <item> take item from the room.\n"
                      "DROP <item> drop item from your inventor.")

            elif command == "QUIT":
                print("Thanks for playing!")
                # Quit game
                return 0

            elif command == "LOOK":
                # Show current room description
                self.current_room.show_description()
                # Show current room inventory, if there is an item
                if len(self.current_room.inventory.items) != 0:
                    self.current_room.inventory.show()

            elif command == "INVENTORY":
                # Show inventory contents
                if len(self.inventory.check()) > 0:
                    self.inventory.show()
                else:
                    print("Your inventory is empty.")

            # If the users wants to take something
            elif "TAKE" in command:
                # Split command
                command = command.split()
                # Make sure user specified an item
                if (len(command)) < 2:
                    print("Specify item")
                else:
                    # Call take function
                    self.take(command[1], self.current_room.id)

            elif "DROP" in command:
                # Split command
                command = [command.split()]
                # Make sure user specified an item

                # Call drop function
                self.drop(command[0][1], self.current_room.id)

            elif self.current_room.is_connected(command):
                # If valid move
                self.move(command)
                # Check if next room is a forced room
                self.forced_check()
                # Print full description only if visiting new rooms
                if int(self.current_room.id) not in visited_rooms:
                    self.current_room.show_description()
                    # If there is an item in the room, print item
                    if len(self.current_room.inventory.items) != 0:
                        self.current_room.inventory.show()
                # Else only print the room name
                else:
                    self.current_room.show_name()
                    # If there is an item print item
                    if len(self.current_room.inventory.items) != 0:
                        self.current_room.inventory.show()
                # Append room to visited_rooms
                visited_rooms.append(int(self.current_room.id))

            else:
                print("Invalid command")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Adventure only takes one command-line argument")
        sys.exit(1)
    try:
        adventure = Adventure(sys.argv[1])
        adventure.play()
    except FileNotFoundError:
        print("Invalid file")
        sys.exit(1)
