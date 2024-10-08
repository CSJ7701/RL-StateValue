import numpy as np
from rl_statevalue import Grid
from rl_statevalue.Direction import Direction

class Agent:
    def __init__(self, environment: Grid.Grid):
        self.position = [0,0] # Row, Column
        self.environment = environment
        # Initialize robot's position in the grid
        self.environment.coords[self.position[0], self.position[1]] = 1

    def move(self, direction: Direction) -> None:
        if not isinstance(direction, Direction):
            raise ValueError(f"Invalid Direction ({direction}). Must be of the 'Direction' class.")
        try:
            moveX = self.position[1]+direction.value[1] # Proposed X coords
            moveY = self.position[0]+direction.value[0] # Proposed Y coords
            self.checkMove((moveY,moveX))
            # Clear current position in environment coordinate grid
            self.environment.coords[self.position[0], self.position[1]] = 0

            self.position[0] = self.position[0]+direction.value[0] # Update Y coords
            self.position[1] = self.position[1]+direction.value[1] # Update X coords

            # Display position in the environment coordinate grid
            self.environment.coords[self.position[0], self.position[1]] = 1

        except ValueError as e:
            print(f"\n[ERROR] Invalid move location.\n{e}")

    def checkMove(self, position: tuple[int,int]) -> None:
        availableSpace: tuple[int,int] = self.environment.coords.shape
        yCoord = position[0]
        xCoord = position[1]
        if xCoord < 0 or yCoord < 0:
            raise ValueError(f"Invalid Coordinate: {position} exceeds bounds of {availableSpace}")
        if xCoord > availableSpace[1]-1 or yCoord > availableSpace[0]-1:
            raise ValueError(f"Invalid Coordinate: {position} exceeds bounds of {availableSpace}")


if __name__ == "__main__":
    GRID_SIZE = 3
    test_grid = Grid.Grid(GRID_SIZE)
    test_agent = Agent(test_grid)
    test_agent.move(Direction.N)
    test_grid.print()
    test_agent.move(Direction.S)
    test_grid.print()
    test_agent.move(Direction.E)
    test_grid.print()
    test_agent.move(Direction.W)
    test_grid.print()
