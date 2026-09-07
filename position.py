import math

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Pos(self.x * other, self.y * other)

    def __str__(self):
        return f"Position({self.x}, {self.y})"

    def __eq__(self, value):
        try:
            return self.x == value.x and self.y == value.y
        except:
            return False # ! skusim to snad nezabudnut zmenit na to, ze ak to porovnavam s niecim co nie je Pos, tak ze dam False

    def tuple(self):
        return (self.x, self.y)

    def vzdialenost_do(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def rotacia_doprava(self):
        return Pos(-self.y, self.x)

    def rotacia_doprava_viac_krat(self, pocet):
        ret = Pos(self.x, self.y)
        for _ in range(pocet):
            ret = ret.rotacia_doprava()
        return ret