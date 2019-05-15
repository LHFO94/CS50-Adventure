class Item(object):
    """
    Representation of an item in Adventure
    """

    def __init__(self, name, description, initial_room_id):
        """
        Initializes an item
        """
        self.name = name
        self.description = description
        self.initial_room_id = initial_room_id

    def get_id(self):
        return self.initial_room_id

    def show(self):
        print(f'{self.name}: {self.description}')

    def __repr__(self):
        return(f'{self.name}: {self.description}')


