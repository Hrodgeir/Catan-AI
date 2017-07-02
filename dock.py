""" Dock Class """
class Dock():
    """ Docks are sometimes associated to coast placements
    """

    def __init__(self, resource):
        self.resource = resource
        if(resource == "all"):
            self.ratio = 3
        else:
            self.ratio = 2

    def get_ratio(self):
        """ Gets the ratio, ratio:1 """
        return self.ratio

    def get_resource(self):
        """ Gets the resource type"""
        return self.resource
