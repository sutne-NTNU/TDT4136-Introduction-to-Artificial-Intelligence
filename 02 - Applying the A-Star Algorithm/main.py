from astar.astar import *
from environment.Samfundet import *

if __name__ == "__main__":
    tasks = [1, 2, 3, 4]
    for task in tasks:
        map = Samfundet(task=task)

        astar = Astar(map)
        astar.find_path()

        astar.visualize_path(filename=f'./images/task_{task}_solved.png')

        astar.visualize_all_steps(path=f'./videos/task_{task}/')
