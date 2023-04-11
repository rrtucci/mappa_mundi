class Node:
    def __init__(self, time, place):
        self.time = time
        self.place = place
        assert time >=0 and place >= 0

    def coords(self):
        return (self.time, self.place)







