import numpy as np

class Grid:
    def __init__(self, dim: int):
        if dim < 0:
            raise ValueError("Dimension must be a non-negative integer.")
        self.DIMENSION = dim
        self.coords = self.initGrid()
        self.states = self.initGrid()
        
    def print(self) -> None:
        print("=== Current Grid ===")
        print(self.coords)
        print()
        print("=== Grid State Values ===")
        print(self.states)

    def initGrid(self) -> np.ndarray:
        dim = self.DIMENSION;
        return np.zeros((dim,dim))
