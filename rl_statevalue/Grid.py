import numpy as np
from Direction import Direction
from pprint import pprint

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
        # Loop through rows
        for i in range(self.DIMENSION):
            row_output = ""
            # Loop through columns in the row
            for j in range(self.DIMENSION):
                # Extract the policy dictionary for the current cell
                policy_dict = self.policy[i][j]
                
                # Create a compact string to represent the policy, for example: "N:0.5 S:1.0 E:0.75 W:0.25"
                policy_str = " ".join([f"{action[0]}:{value:.2f}" for action, value in policy_dict.items()])
                
                # Add the policy string to the row output, formatted nicely
                row_output += f"| {policy_str} |".center(40)  # Adjust width for alignment
                
            # Print the row
            print(row_output)
            print()  # Empty line between rows for readability

    def initGrid(self) -> np.ndarray:
        dim = self.DIMENSION;
        return np.zeros((dim,dim))

    def setRewardsManual(self, reward_values: np.ndarray) -> None:
        """Sets rewards on the grid. Expects a 2D numpy array of shape (DIMENSION, DIMENSION)."""
        if self.rewards_set:
            raise RuntimeError("[ERROR]: Reward values have already been set for this instance.")

        if not isinstance(reward_values, np.ndarray):
            raise TypeError("Reward values must be a numpy array.")
        if reward_values.shape != (self.DIMENSION, self.DIMENSION):
            raise ValueError(f"Reward Values must be a {self.DIMENSION}x{self.DIMENSION} array.")

        self.rewards = reward_values
        self.rewards_set = True

    def setRewards(self, goal: tuple[int, int], goal_value: int, default: int = 0) -> None:
        """
        Sets up the reward matrix for the grid.

        Parameters:
        - goal: a tuple representing the coordinates of the goal (e.g., (x, y)).
        - goal_value: an integer representing the reward value at the goal.
        - default: an integer representing the default reward for all other cells (default is 0).
        """
        if self.rewards_set:
            raise RuntimeError("Rewards have already been set. Cannot reset rewards.")

        # Set the goal coordinate and the reward matrix
        self.Goal = goal
        self.rewards = np.full((self.DIMENSION, self.DIMENSION), default)
    
        # Set the goal value at the specified coordinates
        self.rewards[goal[0], goal[1]] = goal_value
    
        # Mark rewards as set
        self.rewards_set = True


    def updateStates(self, state_values: np.ndarray):
        """Updates the states on the grid. Expects a 2D numpy array of shape (DIMENSION, DIMENSION)."""
        if not isinstance(state_values, np.ndarray):
            raise TypeError("State Values must be a numpy array.")
        if state_values.size != (self.DIMENSION, self.DIMENSION):
            raise ValueError(f"State Values must ba a {self.DIMENSION}x{self.DIMENSION} array.")

        self.states = state_values
