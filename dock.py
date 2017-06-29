""" Dock Class """
class Dock():
    """ Docks are sometimes associated to coast placements
    """

    def __init__(self, dock_type, resource):
        self.dock_type = dock_type
        self.resource = resource

    def get_dock_type(self):
        """ Gets the type of the placement """
        return self.dock_type

    def get_resource(self):
        """ Gets the dice value of the placement """
        return self.resource
