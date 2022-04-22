from environment.Samfundet import Samfundet
from astar.state import State
from astar.node import Node


class Astar:

    def __init__(self, map: Samfundet):
        self.map = map

        self.open: list[Node] = []  # sorted by nodes f-values (cheapest first)
        self.closed: list[Node] = []  # unsorted, contains all visited nodes

        # Define the goal state
        goal_x, goal_y = map.get_goal_pos()
        self.goal_state = State(goal_x, goal_y)

        # initialize start node
        start_x, start_y = map.get_start_pos()
        start_node = Node(State(start_x, start_y))
        start_node.h = self.heuristic(start_node)
        self.open.append(start_node)

        # save solution node when we find it
        self.goal_node = None

    def find_path(self):
        """
        Find the shortest path from the maps given start_pos to its goal_pos, then 
        shows and saves an image displaying the shortest path.
        """
        # Perform the agenda loop
        self.agenda_loop()
        print(f'Found path after checking {len(self.closed)} nodes')

    def agenda_loop(self):
        """
        The main loop that traverses the map and finds the shortest path.
        returns the goal node, to create the path we simply follow each nodes 
        parent until we reach the start node.
        """
        while self.has_open_nodes:

            # When retreiving a node from the queue, that means
            # we have found the shortst path to this node
            current_node = self.open.pop(0)
            self.closed.append(current_node)

            if self.is_goal(current_node):
                # found shortest path to goal
                self.goal_node = current_node
                return

            # Find all connected nodes to this node
            children = self.get_children(current_node)

            for child in children:
                if child in self.closed:
                    # Have already found shortest path to the child
                    continue

                map_value = self.map.get_cell_value(
                    (child.state.x, child.state.y))

                if child not in self.open:
                    # Node has never been seen before
                    child.h = self.heuristic(child)
                    child.g = current_node.g + map_value
                    child.parent = current_node
                else:
                    # Node has been seen before, get stored values
                    child = self.open.pop(self.open.index(child))
                    old_path_length = child.g
                    new_path_length = current_node.g + map_value
                    if new_path_length < old_path_length:
                        # found shorter path, replace old one and parent
                        child.g = new_path_length
                        child.parent = current_node

                self.add_and_sort(child)

        print("Could not find any path from start to end")

    def heuristic(self, node: Node) -> int:
        """
        Estimate the distance from the `node` to the goal_state.
        """
        x_distance = abs(self.goal_state.x - node.state.x)
        y_distance = abs(self.goal_state.y - node.state.y)
        return x_distance + + y_distance

    def has_open_nodes(self) -> bool:
        """
        Check if there still are som nodes in the queue for us to check
        """
        return self.open

    def get_children(self, node) -> 'list[Node]':
        """
        Find all valid Nodes connected to the given node and return them in a list.
        """
        children: list[Node] = []
        for direction in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            x = node.state.x + direction[0]
            y = node.state.y + direction[1]
            map_value = self.map.get_cell_value((x, y))
            if map_value != -1:
                child = Node(State(x, y))
                children.append(child)
        return children

    def is_goal(self, node: Node) -> bool:
        return node.state == self.goal_state

    def add_and_sort(self, node: Node):
        """
        Add the node to `self.open` in its sorted position (based on its f value)
        """
        for index, opened in enumerate(self.open):
            if node.f() < opened.f():
                self.open.insert(index, node)
                return
        self.open.append(node)

    def set_path_map_values(self, value: str):
        """
        Overwrite the map string values (used to draw the map) to empty 
        space in order to be able to draw the map with the path easily.
        """
        node = self.goal_node.parent  # skip goal position
        while node.parent is not None:  # stop before start position
            self.map.set_cell_value((node.state.x, node.state.y), value)
            node = node.parent

    def visualize_path(self, show=True, save=True, filename: str = 'solved.png'):
        """
        Saves the path to the map object and shows it in an image and/or saves it 
        with the given filename
        """
        self.set_path_map_values(" ")
        if(show):
            self.map.show_map()
        if(save):
            self.map.save_map(filename)
        self.set_path_map_values(' . ')

    def visualize_all_steps(self, path: str):
        """
        Show all nodes (tiles) the algorithm checked in an image.
        """
        for i, node in enumerate(self.closed[1:-1]):
            self.map.set_cell_value((node.state.x, node.state.y), " ")
            self.map.save_map(f'{path}{i:03d}.png')
