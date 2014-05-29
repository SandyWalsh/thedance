"""This is just the sequence manager, we have no concept
   of "current direction" ... that's left to the device to
   track. We only care about which direction we should be
   pointing at a given time."""

class Participant(object):
    def __init__(self):
        self.sequence = []
        self.direction = 0

    def add(self, dot):
        self.sequence.append(dot)

    def __str__(self):
        return str(self.direction)


class Grid(object):
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.grid = [[Participant() for x in range(size_x)] for x in range(size_y)]

    def set(self, x, y, direction):
        self.grid[y][x].direction = direction

    def get(self, x, y):
        return self.grid[y][x]

    def move_dots(self):
        pass

    def dump(self):
        for x, row in enumerate(self.grid):
            if x == 0:
                print "  ",
                for y, col in enumerate(row):
                    print "%3d" % y,
                print
            for y, col in enumerate(row):
                if y == 0:
                    print "%d." % x,
                print "%3s" % str(col),
            print


grid = Grid(5, 5)
grid.dump()


class Movement(object):
    def __init__(self):
        self.target_direction = direction  # 0-359
        self.movement = 0  # +1 (clockwise) or -1 (counter clockwise)
        self.speed = 0  # degrees per tick

        self.ticks = 250  # ms

    def _distance_to_target(self, moving):
        """Compute the distance to the target if
           we're moving in a clockwise or counterclockwise
           direction."""
        direction = self.participant.direction
        if moving > 0:
            if direction < self.target_direction:
                return 360 - direction + self.target_direction
            return self.target_direction - direction
        else:
            if direction < self.target_direction:
                return direction - self.target_direction
            return 360 - self.target_direction + direction

    def move_to_direction(self, target_direction, movement, millis):
        # millis = 250 would mean instant transportation to target.
        if millis < self.ticks:
            raise Exception("Smallest time is %dms" % self.ticks)
        self.target_direction = target_direction
        self.movement = movement
        self.speed = self._distance_to_target(movement) / (millis / self.ticks)

    def start(self, participant):
        self.participant = participant

    def increment(self):
        self.participant.direction + (self.speed * self.movement)
