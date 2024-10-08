import numpy as np
from rl_statevalue.Direction import Direction

class Grid:
    def __init__(self, dim: int):
        if dim < 0:
            raise ValueError("Dimension must be a non-negative integer.")
        self.DIMENSION = dim
        self.coords = self.initGrid()
        self.states = self.initGrid()
        self.rewards = self.initGrid()
        self.rewards_set = False

        # Initialize policy as a DIMENSION by DIMENSION grid of dictionaries
        self.policy = [[{action.name: (1/len(Direction)) for action in Direction} for _ in range(self.DIMENSION)] for _ in range(self.DIMENSION)]
        
    def print(self) -> None:
        print("=== Current Grid ===")
        print(self.coords)
        print()
        print("=== Grid State Values ===")
        print(self.states)
        print()
        print("=== Reward Values ===")
        print(self.rewards)
        print()
        print("=== Policy Values ===")
        print(self.policy)

    def initGrid(self) -> np.ndarray:
        dim = self.DIMENSION;
        return np.zeros((dim,dim))

    def setRewards(self, reward_values: np.ndarray) -> None:
        """Sets rewards on the grid. Expects a 2D numpy array of shape (DIMENSION, DIMENSION)."""
        if self.rewards_set:
            raise RuntimeError("[ERROR]: Reward values have already been set for this instance.")

        if not isinstance(reward_values, np.ndarray):
            raise TypeError("Reward values must be a numpy array.")
        if reward_values.shape != (self.DIMENSION, self.DIMENSION):
            raise ValueError(f"Reward Values must be a {self.DIMENSION}x{self.DIMENSION} array.")

        self.rewards = reward_values
        self.rewards_set = True

    def updateStates(self, state_values: np.ndarray):
        """Updates the states on the grid. Expects a 2D numpy array of shape (DIMENSION, DIMENSION)."""
        if not isinstance(state_values, np.ndarray):
            raise TypeError("State Values must be a numpy array.")
        if state_values.size != (self.DIMENSION, self.DIMENSION):
            raise ValueError(f"State Values must ba a {self.DIMENSION}x{self.DIMENSION} array.")

        self.states = state_values
