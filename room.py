from inventory import Inventory

class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description, directions=None, inventory=None):
        """
        Initializes a Room
        """
        self.id = id
        self.name = name
        self.description = description
        self.directions = {}
        self.inventory = Inventory()

    def add_route(self, connection, room):
        """
        Adds a given direction and the connected room to our room object.
        """
        if connection not in self.directions:
            self.directions[connection] = room
        else:
            value = self.directions[connection]
            if type(value) == list:
                value.append(room)
            else:
                self.directions[connection] = [value, room]

    def is_connected(self, direction):
        """
        Checks whether the given direction has a connection from a room.
        Returns a boolean.
        """
        if direction in self.directions.keys():
            return True
        else:
            return False

    def show_description(self):
        print(f'{self.description}')

    def show_name(self):
        print(f'{self.name}')

    def __str__ (self):
        return(f'Room number: {self.id} , Directions: {self.directions}')
