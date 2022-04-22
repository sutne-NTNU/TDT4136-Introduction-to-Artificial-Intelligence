from astar.state import State


class Node:

    def __init__(self, state: State):
        self.state: State = state  # Coordinate (x, y)

        self.parent: Node = None  # best parent

        self.g = 0  # cost from start to this node
        self.h = 0  # estimated cost from this node to the goal

    def f(self):
        """
        Estimated total distance from start node to goal through this node.
        """
        return self.g + self.h

    def __eq__(self, other: any):
        return self.state == other.state

    def __ne__(self, other: any):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return f'Node: {str(self.state)} g: {self.g} h: {self.h} f: {self.f}'
