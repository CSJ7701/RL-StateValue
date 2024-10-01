from enum import Enum

class Direction(Enum):
    N = (1,0)
    S = (-1,0)
    E = (0,1)
    W = (0,-1)

class Agent:
    def __init__(self):
        ...

    def move(self, direction: Direction) -> None:
        if not isinstance(direction, Direction):
            raise ValueError(f"Invalid Direction ({direction}). Must be of the 'Direction' class.")
        print(f"Direction: {direction.name}")
        
