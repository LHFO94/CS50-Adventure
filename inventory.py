class Inventory(object):
    """
    Representation of an inventory in Adventure
    """

    def __init__(self):
        """
        Initializes an inventory
        """
        self.items = {}

    def add(self, item):
        """
        Adds an item to the inventory
        """

        self.items[item.name] = item.description

    def remove(self, item):
        """
        Removes an item from the inventory
        """

        del self.items[item]

    def show(self):
        """
        displays the items in inventory
        """
        for item, description in self.items.items():
            print("{} : {}".format(item, description))

    def check(self):
        return self.items

    def __repr__(self):
        return(f'{self.items}')