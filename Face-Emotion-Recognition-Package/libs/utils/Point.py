
class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def X(self):
        return self.x

    def Y(self):
        return self.y

    def toString(self):
        x = self.x
        y = self.y

        # Header
        text = "{"

        # Body
        text += "\"x\": " + str(x)

        text += ", "

        text += "\"y\": " + str(y)

        # Footer
        text += "}"

        return text




# point = Point(1, 1)
#
# print(point)
# print(point.x, point.y)
# print("{}, {}".format(point.X(), point.Y()))
#
# point.x = 2
# point.y = 2
#
# print(point)
# print(point.x, point.y)
# print("{}, {}".format(point.X(), point.Y()))

