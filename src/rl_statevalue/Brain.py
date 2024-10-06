import numpy as np
from rl_statevalue.Agent import Agent, Direction
from rl_statevalue.Grid import Grid

class Brain():
    def __init__(self, agent: Agent, grid: Grid, discount_factor: float = 0.7) :
        self.Agent = agent 
        self.Grid = grid 
        self.Gamma = discount_factor
        

    def updateStateValues(self) -> None:
        """Update state values using Bellman's Equation"""
        new_state_values = np.copy(self.Grid.states)
        for i in range(self.Grid.DIMENSION-1):
            for j in range(self.Grid.DIMENSION-1):
                current_position = (i,j)
                print(f"[*LOG*] Calculating value for state {current_position}")
                total_state_value = 0

                for action in Direction:
                    # Get next state (N) and probability (P)
                    N = self.getNextState(current_position, action)
                    R = self.getReward((N[0],N[1]))
                    P = self.getPolicy()
                    state_action_value = P*(R+(self.Gamma*self.Grid.states[N[0], N[1]]))
                    total_state_value += state_action_value
                new_state_values[i,j]=total_state_value
                print(f"[LOG] State Value for {current_position} = {total_state_value}")
        self.Grid.states = new_state_values
            

    def getNextState(self, position: tuple[int,int], action: Direction) -> tuple[int, int]:
        """Returns the next state (as a tuple coordinate) based on current position and action."""
        delta = action.value
        new_position = (position[0]+delta[0], position[1]+delta[1])
        print(f"[LOG] Next State at Position: {new_position}")
        if (new_position[0] >= 3 or new_position[1] >= 3):
            raise ValueError(f"[ERROR] State {new_position} is out of bounds")
        return (position[0]+delta[0], position[1]+delta[1])

    def getReward(self, position: tuple[int,int]):
        """Returns the reward for a given coordinate"""
        if not self.Grid.rewards_set:
            raise ValueError("Rewards have not been specified. Please initialize using '[grid_variable].setRewards([numpy array])'")

        # Check if the agent will "bounce"
        if (position[0] < 0 or position[0] >= self.Grid.rewards.shape[0] or position[1] < 0 or position[1] >= self.Grid.rewards.shape[1]):
            return -1
        
        return self.Grid.rewards[position[0],position[1]]

    def getPolicy(self) -> float:
        return 0.25

    def updatePolicy(self) -> None:
        ... 


if __name__ == "__main__":
    test_grid = Grid(2)
    test_agent = Agent(test_grid)
    test_grid.setRewards(np.array([[0,5],[0,0]]))
    # test_grid.setRewards(np.array([[0,0,5],[0,0,0],[0,0,0]]))
    test_brain = Brain(test_agent, test_grid)

    test_brain.updateStateValues()
    test_grid.print()
